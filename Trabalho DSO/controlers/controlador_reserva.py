from entidades.reserva import Reserva
from entidades.servico_de_quarto import ServicoDeQuarto
from entidades.pet import Pet
from telas.tela_reserva import TelaReserva
from controlers.controlador_hospede import ControladorHospede
from controlers.controlador_quartos import ControladorQuarto
from controlers.controlador_funcionario import ControladorFuncionario
from controlers.ValidacaoException import ValidacaoException
from controlers.ReservaException import ReservaException
from typing import List, Optional


class ControladorReserva:
    def __init__(self, controlador_hospede: ControladorHospede, controlador_quarto: ControladorQuarto,
                 controlador_funcionario: ControladorFuncionario):
        self.__reservas: list[Reserva] = []
        self.__tela = TelaReserva()
        self.__controlador_hospede = controlador_hospede
        self.__controlador_quarto = controlador_quarto
        self.__controlador_funcionario = controlador_funcionario

    def abre_tela(self):
        opcoes = {
            1: self.fazer_reserva,
            2: self.listar_reservas,
            3: self.cancelar_reserva,
            4: self.editar_reserva,
            5: self.adicionar_servico_a_reserva,
            6: self.adicionar_pet_a_reserva,
            7: self.calcular_valor_total_reserva,
            8: self.exibir_relatorio_por_hospede,
            9: self.exibir_relatorio_por_tipo_servico,
            0: self.retornar
        }
        while True:
            try:
                opcao = self.__tela.tela_opcoes()
                opcoes[opcao]()
                if opcao == 0:
                    break
            except ReservaException as e:
                self.__tela.mostra_mensagem(f"❌ Erro de reserva: {e}")
            except ValidacaoException as e:
                self.__tela.mostra_mensagem(f"⚠️ Erro de validação: {e}")
            except Exception as e:
                self.__tela.mostra_mensagem(f"🔥 Erro inesperado: {e}")

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")

    def fazer_reserva(self):
        try:
            dados_reserva = self.__tela.pega_dados_reserva()
            if not dados_reserva:
                raise ValidacaoException("Criação de reserva cancelada pelo usuário.")

            hospedes_encontrados = []
            for cpf in dados_reserva["cpfs_hospedes"]:
                hospede = self.__controlador_hospede.busca_hospede(cpf)
                if not hospede:
                    raise ReservaException(f"Hóspede com CPF {cpf} não encontrado.")
                hospedes_encontrados.append(hospede)

            if not hospedes_encontrados:
                raise ReservaException("Nenhum hóspede válido selecionado.")

            quartos_selecionados = []
            for numero_quarto in dados_reserva["numeros_quartos"]:
                quarto = self.__controlador_quarto.buscar_quarto(int(numero_quarto))
                if not quarto:
                    raise ReservaException(f"Quarto {numero_quarto} não existe.")

                if not quarto.disponibilidade:
                    raise ReservaException(f"Quarto {numero_quarto} está indisponível.")

                quartos_selecionados.append(quarto)

            nova_reserva = Reserva(
                hospedes=hospedes_encontrados,
                quartos=quartos_selecionados,
                data_checkin=dados_reserva["data_checkin"],
                data_checkout=dados_reserva["data_checkout"]
            )

            conflicto = nova_reserva.reservar_quartos()
            if conflicto:  # se True = ERRO
                raise ReservaException("O quarto não pôde ser reservado (possível overlap).")

            self.__reservas.append(nova_reserva)
            self.__tela.mostra_mensagem(f"✅ Reserva ID {nova_reserva.id} criada com sucesso!")
            self.__tela.mostra_mensagem(nova_reserva.get_all_data())

        except (ValidacaoException, ReservaException):
            raise
        except Exception as e:
            raise ReservaException(f"Erro inesperado ao criar reserva: {e}")

    def listar_reservas(self):
        if not self.__reservas:
            self.__tela.mostra_mensagem("Nenhuma reserva cadastrada.")
            return
        lista_str = [str(reserva) for reserva in self.__reservas]
        self.__tela.mostra_lista_reservas(lista_str)

    def _selecionar_reserva(self, reserva_identificador=None) -> Optional[Reserva]:
        try:
            if not reserva_identificador:
                reserva_identificador = self.__tela.seleciona_reserva()

            if not reserva_identificador:
                raise ValidacaoException("Seleção de reserva cancelada.")

            try:
                reserva_id = int(reserva_identificador)
                for reserva in self.__reservas:
                    if reserva.id == reserva_id:
                        return reserva
            except ValueError:
                pass

            encontradas = [
                r for r in self.__reservas
                if r.hospedes and reserva_identificador.lower() in r.hospedes[0].nome.lower()
            ]

            if len(encontradas) == 1:
                return encontradas[0]
            if len(encontradas) > 1:
                raise ReservaException("Múltiplas reservas encontradas. Utilize o ID.")
            raise ReservaException("Reserva não encontrada.")

        except (ValidacaoException, ReservaException):
            raise
        except Exception as e:
            raise ReservaException(f"Erro inesperado ao buscar reserva: {e}")

    def cancelar_reserva(self):
        try:
            reserva = self._selecionar_reserva()
            confirmar = self.__tela.le_string("Confirmar cancelamento? (sim/nao): ")

            if confirmar.lower() != "sim":
                raise ValidacaoException("Cancelamento não confirmado.")

            reserva.liberar_quartos()
            self.__reservas.remove(reserva)
            self.__tela.mostra_mensagem("Reserva cancelada.")

        except (ValidacaoException, ReservaException):
            raise
        except Exception as e:
            raise ReservaException(f"Erro inesperado ao cancelar reserva: {e}")

    def editar_reserva(self):
        reserva = self._selecionar_reserva()
        dados = self.__tela.pega_dados_edicao()

        try:
            if not dados:
                raise ValidacaoException("Edição cancelada.")

            novos_quartos_obj = None

            if dados["limpar_quartos"]:
                novos_quartos_obj = []
            elif dados["novos_numeros_quartos"]:
                novos_quartos_obj = []
                for numero in dados["novos_numeros_quartos"]:
                    quarto = self.__controlador_quarto.buscar_quarto(int(numero))
                    if not quarto:
                        raise ReservaException(f"Quarto {numero} não existe.")
                    if not quarto.disponibilidade and quarto not in reserva.quartos:
                        raise ReservaException(f"Quarto {numero} indisponível.")
                    novos_quartos_obj.append(quarto)

            reserva.editar_reserva(
                nova_data_checkin=dados["nova_data_checkin"],
                nova_data_checkout=dados["nova_data_checkout"],
                novos_quartos=novos_quartos_obj
            )

            self.__tela.mostra_mensagem("Reserva editada com sucesso.")

        except (ValidacaoException, ReservaException):
            raise
        except Exception as e:
            raise ReservaException(f"Erro inesperado ao editar: {e}")

    def adicionar_servico_a_reserva(self):
        try:
            reserva = self._selecionar_reserva()
            dados = self.__tela.pega_dados_servico()
            if not dados:
                raise ValidacaoException("Operação cancelada.")

            quarto = None
            for q in reserva.quartos:
                if q.numero == int(dados["numero_quarto"]):
                    quarto = q
                    break
            if not quarto:
                raise ReservaException("Quarto não faz parte da reserva.")

            funcionario = self.__controlador_funcionario.buscar_funcionario(dados["cpf_funcionario"])
            if not funcionario:
                raise ReservaException("Funcionário não encontrado.")

            servico = ServicoDeQuarto(
                quarto=quarto,
                funcionario=funcionario,
                tipo_servico=dados["tipo_servico"],
                valor=dados["valor"]
            )

            reserva.adicionar_servico_quarto(servico)
            self.__tela.mostra_mensagem("Serviço adicionado.")

        except (ValidacaoException, ReservaException):
            raise
        except Exception as e:
            raise ReservaException(f"Erro inesperado ao adicionar serviço: {e}")

    def adicionar_pet_a_reserva(self):
        try:
            reserva = self._selecionar_reserva()

            hospede = self.__controlador_hospede.busca_hospede()
            nome_pet = self.__tela.le_string("Nome do pet: ")
            pet = hospede.busca_pet(nome_pet)

            reserva.adicionar_pet(pet)
            for quarto in reserva.quartos:
                quarto.adicionar_pet(pet)

            self.__tela.mostra_mensagem("Pet adicionado à reserva.")

        except (ValidacaoException, ReservaException):
            raise
        except Exception as e:
            raise ReservaException(f"Erro inesperado ao adicionar pet: {e}")

    def calcular_valor_total_reserva(self):
        reserva = self._selecionar_reserva()
        reserva.calcular_valor_total()
        self.__tela.mostra_mensagem(f"Valor total: R$ {reserva.valor_total:.2f}")

    def exibir_relatorio_por_hospede(self):
        if not self.__reservas:
            raise ValidacaoException("Nenhuma reserva cadastrada.")

        relatorio = []
        hospedes_reservas = {}

        for reserva in self.__reservas:
            for hospede in reserva.hospedes:
                hospedes_reservas.setdefault(hospede.cpf, {"nome": hospede.nome, "ids": []})
                hospedes_reservas[hospede.cpf]["ids"].append(reserva.id)

        for cpf, info in hospedes_reservas.items():
            relatorio.append(
                f"{info['nome']} (CPF {cpf}) -> Reservas: {', '.join(map(str, info['ids']))}"
            )

        self.__tela.mostra_lista(relatorio)

    def exibir_relatorio_por_tipo_servico(self):
        if not self.__reservas:
            raise ValidacaoException("Nenhuma reserva cadastrada.")

        servicos = {}
        for reserva in self.__reservas:
            for servico in reserva.servicos_quarto:
                tipo = servico.tipo_servico
                servicos[tipo] = servicos.get(tipo, 0) + 1

        if not servicos:
            self.__tela.mostra_mensagem("Nenhum serviço registrado.")
            return

        relatorio = [f"{k}: {v}x" for k, v in servicos.items()]
        self.__tela.mostra_lista(relatorio)

    @property
    def reservas(self) -> List[Reserva]:
        return self.__reservas
