from entidades.quartos import Suite, Duplo, Simples
from entidades.quarto import Quarto
from telas.tela_quarto import TelaQuarto
from controlers.ValidacaoException import ValidacaoException
from typing import Optional, Dict, Any
from daos.quarto_dao import QuartoDAO
from daos.reserva_dao import ReservaDAO


class ControladorQuarto:
    def __init__(self):
        self.__tela = TelaQuarto()
        self.__quarto_dao = QuartoDAO()

        self.__mapa_tipos = {
            "suite": Suite,
            "duplo": Duplo,
            "simples": Simples
        }

        self.__valores_diaria = {
            "suite": 300.0,
            "duplo": 200.0,
            "simples": 100.0
        }

    def abre_tela(self):
        opcoes = {
            1: self.cadastrar_quarto,
            2: self.listar_quartos,
            3: self.alterar_quarto,
            4: self.excluir_quarto,
            0: self.retornar
        }

        while True:
            try:
                opcao = self.__tela.tela_opcoes()
                if opcao in opcoes:
                    opcoes[opcao]()
                    if opcao == 0:
                        break
                else:
                    self.__tela.mostra_mensagem("Opção inválida.")
            except Exception as e:
                self.__tela.mostra_mensagem(f"Erro no sistema: {e}")

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")

    def buscar_quarto(self, numero: int) -> Quarto | None:
        try:
            ValidacaoException.validar_campo_vazio(str(numero), "Número do Quarto")
        except ValidacaoException:
            return None

        return self.__quarto_dao.get(numero)

    def cadastrar_quarto(self):
        try:
            dados: Optional[Dict[str, Any]] = self.__tela.pega_dados_quarto(modo=None)
            if dados is None:
                self.__tela.mostra_mensagem("Cadastro cancelado.")
                return

            numero = dados["numero"]

            if self.buscar_quarto(numero):
                raise ValidacaoException(f"O quarto nº {numero} já está cadastrado.")

            tipo = dados["tipo"].lower()
            ClasseQuarto = self.__mapa_tipos.get(tipo)

            if not ClasseQuarto:
                raise ValidacaoException("Tipo de quarto inválido.")

            valor_diaria = self.__valores_diaria[tipo]

            if tipo == "suite":
                quarto = ClasseQuarto(numero, True, dados.get("hidro", False))
            else:
                quarto = ClasseQuarto(numero, True)

            quarto.valor_diaria = valor_diaria


            self.__quarto_dao.add(quarto)

            self.__tela.mostra_mensagem(
                f"Quarto {quarto.numero} ({tipo.upper()}) cadastrado com sucesso."
            )

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado: {e}")

    def listar_quartos(self):
        quartos = self.__quarto_dao.get_all()

        if not quartos:
            self.__tela.mostra_mensagem("Nenhum quarto cadastrado.")
            return

        dados_para_tabela = []

        for quarto in quartos:
            tipo = type(quarto).__name__.lower()

            quarto_dict = {
                'numero': quarto.numero,
                'tipo': tipo,
                'disponibilidade': True,
                'hidro': quarto.hidro if isinstance(quarto, Suite) else False
            }

            dados_para_tabela.append(quarto_dict)

        self.__tela.mostra_lista(dados_para_tabela)

    def alterar_quarto(self):
        try:
            numero = self.__tela.seleciona_quarto()
            if numero is None:
                self.__tela.mostra_mensagem("Alteração cancelada.")
                return

            quarto = self.buscar_quarto(numero)
            if not quarto:
                raise ValidacaoException(f"Quarto nº {numero} não encontrado.")

            tipo_existente = type(quarto).__name__.lower()

            dados_atuais = {
                "numero": quarto.numero,
                "tipo": tipo_existente,
                "disponibilidade": True,
                "hidro": quarto.hidro if isinstance(quarto, Suite) else False
            }

            novos_dados = self.__tela.pega_dados_quarto("alt", dados_atuais)
            if novos_dados is None:
                self.__tela.mostra_mensagem("Alteração cancelada.")
                return

            if isinstance(quarto, Suite):
                quarto.hidro = novos_dados["hidro"]

            self.__quarto_dao.update(quarto)
            self.__tela.mostra_mensagem("Quarto alterado com sucesso.")

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado: {e}")

    def excluir_quarto(self):
        try:
            numero = self.__tela.seleciona_quarto()
            if numero is None:
                self.__tela.mostra_mensagem("Exclusão cancelada.")
                return

            quarto = self.buscar_quarto(numero)
            if not quarto:
                raise ValidacaoException(f"Quarto nº {numero} não encontrado.")

            self.__quarto_dao.remove(numero)
            self.__tela.mostra_mensagem("Quarto excluído com sucesso.")

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")

    def verificar_disponibilidade_periodo(self, quarto_or_numero, data_entrada, data_saida, reserva_sendo_editada=None):
        """
        Verifica se o quarto (objeto ou número) está livre no período informado.
        Consulta todas as reservas via ReservaDAO (não usa quarto.reservas).
        Retorna True se disponível, False se houver conflito.
        """
        try:
            if hasattr(quarto_or_numero, "numero"):
                numero_quarto = quarto_or_numero.numero
            else:
                numero_quarto = int(quarto_or_numero)

            reserva_dao = ReservaDAO()
            todas_reservas = list(reserva_dao.get_all())  

            for reserva in todas_reservas:
                if reserva_sendo_editada and reserva.id == getattr(reserva_sendo_editada, "id", None):
                    continue

                if not any(getattr(q, "numero", None) == numero_quarto for q in reserva.quartos):
                    continue

                if (data_entrada < reserva.data_checkout) and (data_saida > reserva.data_checkin):
                    return False

            return True

        except Exception:
            return False
