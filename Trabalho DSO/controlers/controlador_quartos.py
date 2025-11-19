from entidades.quartos import Suite, Duplo, Simples
from entidades.quarto import Quarto
from telas.tela_quarto import TelaQuarto
from controlers.ValidacaoException import ValidacaoException
from typing import Optional, Dict, Any, List


class ControladorQuarto:
    def __init__(self):
        self.__quartos: list[Quarto] = []
        self.__tela = TelaQuarto()

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
                self.__tela.mostra_mensagem(f"Um erro ocorreu no sistema: {e}")

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")

    def buscar_quarto(self, numero: int) -> Quarto | None:
        try:
            ValidacaoException.validar_campo_vazio(str(numero), "Número do Quarto")
        except ValidacaoException:

            return None

        for quarto in self.__quartos:
            if quarto.numero == numero:
                return quarto
        return None

    def _get_hospede_nome(self, quarto: Quarto) -> str:

        if quarto.disponibilidade:
            return "Vago"
        else:
            return "Ocupado"

    def cadastrar_quarto(self):
        try:
            dados: Optional[Dict[str, Any]] = self.__tela.pega_dados_quarto(modo=None)
            
            if dados is None:
                 self.__tela.mostra_mensagem("Cadastro de quarto cancelado.")
                 return

            numero: int = dados["numero"]

            if self.buscar_quarto(numero):
                raise ValidacaoException(f"O quarto nº {numero} já está cadastrado.")

            tipo = dados["tipo"].lower()
            ClasseQuarto = self.__mapa_tipos.get(tipo)

            if not ClasseQuarto:
                raise ValidacaoException("Tipo de quarto inválido.")

            valor_diaria = self.__valores_diaria[tipo]
            disponibilidade = True

            if tipo == "suite":
                hidro: bool = dados.get("hidro", False)
                quarto = ClasseQuarto(numero, disponibilidade, hidro)
            else:
                quarto = ClasseQuarto(numero, disponibilidade)

            quarto.valor_diaria = valor_diaria
            self.__quartos.append(quarto)

            self.__tela.mostra_mensagem(
                f"Quarto {quarto.numero} ({tipo.upper()}) cadastrado com sucesso."
            )

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"Erro de validação: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado: {e}")

    def listar_quartos(self):
        if not self.__quartos:
            self.__tela.mostra_mensagem("Nenhum quarto cadastrado.")
            return

        dados_para_tabela: List[Dict[str, Any]] = []

        for quarto in self.__quartos:
            tipo = type(quarto).__name__.lower()
            
            quarto_dict = {
                'numero': quarto.numero,
                'tipo': tipo,
                'disponibilidade': quarto.disponibilidade,
                'hospede_nome': self._get_hospede_nome(quarto),

                'hidro': False 
            }

            if isinstance(quarto, Suite):
                quarto_dict['hidro'] = quarto.hidro

            dados_para_tabela.append(quarto_dict)

        self.__tela.mostra_lista(dados_para_tabela)

    def alterar_quarto(self):
        try:
            numero = self.__tela.seleciona_quarto()
            
            if numero is None:
                self.__tela.mostra_mensagem("Alteração de quarto cancelada.")
                return

            quarto = self.buscar_quarto(numero)

            if not quarto:
                raise ValidacaoException(f"Quarto nº {numero} não encontrado.")

            tipo_existente = type(quarto).__name__.lower()

            dados_atuais = {
                "numero": quarto.numero,
                "tipo": tipo_existente,
                "disponibilidade": quarto.disponibilidade,
                "hidro": quarto.hidro if isinstance(quarto, Suite) else False
            }

            novos_dados: Optional[Dict[str, Any]] = self.__tela.pega_dados_quarto("alt", dados_atuais)
            
            if novos_dados is None:
                self.__tela.mostra_mensagem("Alteração de quarto cancelada.")
                return

            quarto.disponibilidade = novos_dados["disponibilidade"]

            if isinstance(quarto, Suite):
                quarto.hidro = novos_dados["hidro"]

            self.__tela.mostra_mensagem(f"Quarto {quarto.numero} alterado com sucesso.")

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"Erro de validação: {e}")
        except Exception as e:
             self.__tela.mostra_mensagem(f"Erro inesperado: {e}")

    def excluir_quarto(self):
        try:
            numero = self.__tela.seleciona_quarto()
            
            if numero is None:
                self.__tela.mostra_mensagem("Exclusão de quarto cancelada.")
                return

            quarto = self.buscar_quarto(numero)

            if not quarto:
                raise ValidacaoException(f"Quarto nº {numero} não encontrado.")
            
            self.__quartos.remove(quarto)
            self.__tela.mostra_mensagem(f"Quarto {quarto.numero} excluído com sucesso.")

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")

    def verificar_disponibilidade_periodo(self, quarto, data_entrada, data_saida):
        if not hasattr(quarto, "reservas"):
            quarto.reservas = []

        for reserva in quarto.reservas:
            if (data_entrada <= reserva.data_saida) and \
               (data_saida >= reserva.data_entrada):
                return False

        return True
