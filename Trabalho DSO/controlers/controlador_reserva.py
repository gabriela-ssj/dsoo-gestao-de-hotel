from entidades.reserva import Reserva
from entidades.hospede import Hospede
from entidades.quarto import Quarto
from entidades.funcionario import Funcionario
from entidades.servico_de_quarto import ServicoDeQuarto
from entidades.pet import Pet
from telas.tela_reserva import TelaReserva
from typing import List, Optional
from controlers.controlador_hospede import ControladorHospede
from controlers.controlador_quartos import ControladorQuarto
from controlers.controlador_funcionario import ControladorFuncionario
from controlers.ValidacaoException import ValidacaoException
from controlers.ReservaException import ReservaException


class ControladorReserva:
    def __init__(
        self,
        controlador_hospede: ControladorHospede,
        controlador_quarto: ControladorQuarto,
        controlador_funcionario: ControladorFuncionario
    ):
        self.__reservas: List[Reserva] = []
        self.__tela = TelaReserva()
        self.__controlador_hospede = controlador_hospede
        self.__controlador_quarto = controlador_quarto
        self.__controlador_funcionario = controlador_funcionario

    def abre_tela(self):
        lista_opcoes = {
            1: self.fazer_reserva,
            2: self.listar_reservas,
            3: self.cancelar_reserva,
            4: self.alterar_reserva,
            5: self.adicionar_servico_quarto_reserva,
            6: self.adicionar_pet_reserva,
            7: self.mostrar_valor_total_reserva,
            8: self.gerar_relatorio_hospede,
            9: self.gerar_relatorio_tipo_servico,
            0: self.retornar
        }

        while True:
            try:
                opcao = self.__tela.tela_opcoes()
                funcao = lista_opcoes.get(opcao)

                if funcao:
                    funcao()
                    if opcao == 0:
                        break
                else:
                    self.__tela.mostra_mensagem("Opção inválida.")
            except (ReservaException, ValidacaoException) as e:
                self.__tela.mostra_mensagem(str(e))
            except Exception as e:
                self.__tela.mostra_mensagem(f"Erro inesperado: {e}")

    def retornar(self):
        pass


    def fazer_reserva(self):
        try:
            dados = self.__tela.pega_dados_reserva()
            if not dados:
                raise ValidacaoException("Criação cancelada.")

            cpfs = dados["hospedes_cpfs"]
            numeros = dados["quartos_ids"]
            checkin = dados["checkin_data"]
            checkout = dados["checkout_data"]

            hospedes = []
            for cpf in cpfs:
                hosp = self.__controlador_hospede.busca_hospede(cpf)
                if not hosp:
                    raise ReservaException(f"Hóspede CPF {cpf} não encontrado.")
                hospedes.append(hosp)

            quartos = []
            for num in numeros:
                quarto = self.__controlador_quarto.buscar_quarto(num)
                if not quarto:
                    raise ReservaException(f"Quarto {num} não existe.")
                if not quarto.disponibilidade:
                    raise ReservaException(f"Quarto {num} está indisponível.")

                if not self.__controlador_quarto.verificar_disponibilidade_periodo(
                    quarto, checkin, checkout
                ):
                    raise ReservaException(
                        f"Quarto {num} não está disponível no período."
                    )
                quartos.append(quarto)

            reserva = Reserva(
                hospedes=hospedes,
                quartos=quartos,
                data_checkin=checkin,
                data_checkout=checkout
            )

            reserva.reservar_quartos()
            self.__reservas.append(reserva)

            self.__tela.mostra_mensagem(
                f"✅ Reserva ID {reserva.id} criada com sucesso!"
            )

        except (ReservaException, ValidacaoException) as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")


    def selecionar_reserva(self) -> Optional[Reserva]:
        try:
            identificador = self.__tela.seleciona_reserva()
            if not identificador:
                raise ValidacaoException("Busca cancelada.")

            try:
                id_num = int(identificador)
                for r in self.__reservas:
                    if r.id == id_num:
                        return r
                raise ReservaException("Nenhuma reserva encontrada com esse ID.")
            except ValueError:
                pass

            filtro = identificador.lower()
            resultados = [r for r in self.__reservas
                          if filtro in r.hospedes[0].nome.lower()]

            if len(resultados) == 1:
                return resultados[0]
            if len(resultados) > 1:
                raise ReservaException("Mais de uma reserva encontrada. Use o ID.")
            raise ReservaException("Nenhuma reserva encontrada para esse nome.")

        except (ReservaException, ValidacaoException) as e:
            self.__tela.mostra_mensagem(str(e))
            return None


    def listar_reservas(self):
        if not self.__reservas:
            self.__tela.mostra_mensagem("Nenhuma reserva cadastrada.")
            return

        dados = [r.get_all_data() for r in self.__reservas]
        self.__tela.mostra_reservas(dados)

 
    def cancelar_reserva(self):
        reserva = self.selecionar_reserva()
        if not reserva:
            return

        nomes = ", ".join(h.nome for h in reserva.hospedes)

        if self.__tela.confirma_cancelamento(reserva.id, nomes):
            reserva.status = "cancelada"
            reserva.liberar_quartos()
            self.__tela.mostra_mensagem("Reserva cancelada.")
        else:
            self.__tela.mostra_mensagem("Cancelamento não confirmado.")


    def alterar_reserva(self):
        try:
            reserva = self.selecionar_reserva()
            if not reserva:
                return

            atuais = {
                "hospedes_cpfs": [h.cpf for h in reserva.hospedes],
                "quartos_ids": [q.numero for q in reserva.quartos],
                "checkin": reserva.data_checkin,
                "checkout": reserva.data_checkout
            }

            dados = self.__tela.pega_dados_reserva(modo="alteracao", dados_atuais=atuais)
            if not dados:
                raise ValidacaoException("Alteração cancelada.")

            novos_hosp = []
            for cpf in dados["hospedes_cpfs"]:
                h = self.__controlador_hospede.busca_hospede(cpf)
                if not h:
                    raise ReservaException(f"Hóspede CPF {cpf} não encontrado.")
                novos_hosp.append(h)

            novos_quartos = []
            for num in dados["quartos_ids"]:
                q = self.__controlador_quarto.buscar_quarto(num)
                if not q:
                    raise ReservaException(f"Quarto {num} não existe.")

                if not self.__controlador_quarto.verificar_disponibilidade_periodo(
                    q, dados["checkin_data"], dados["checkout_data"],
                    reserva_sendo_editada=reserva
                ):
                    raise ReservaException(f"Quarto {num} indisponível no período.")

                novos_quartos.append(q)

            reserva.editar_reserva(
                nova_data_checkin=dados["checkin_data"],
                nova_data_checkout=dados["checkout_data"],
                novos_hospedes=novos_hosp,
                novos_quartos=novos_quartos
            )

            self.__tela.mostra_mensagem(
                f"Reserva ID {reserva.id} atualizada. Novo valor: R$ {reserva.valor_total:.2f}"
            )

        except (ReservaException, ValidacaoException) as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")

    def adicionar_servico_quarto_reserva(self):
        try:
            reserva = self.selecionar_reserva()
            if not reserva:
                return

            dados = self.__tela.pega_dados_servico_quarto()
            if not dados:
                raise ValidacaoException("Operação cancelada.")

            func = self.__controlador_funcionario.buscar_funcionario(dados["cpf_funcionario"])
            if not func:
                raise ReservaException("Funcionário não encontrado.")

            quarto = next((q for q in reserva.quartos if q.numero == dados["num_quarto"]), None)
            if not quarto:
                raise ReservaException("Esse quarto não pertence à reserva.")

            servico = ServicoDeQuarto(
                tipo_servico=dados["tipo_servico"],
                valor=dados["valor"],
                quarto=quarto,
                funcionario=func
            )

            reserva.adicionar_servico_quarto(servico)

            self.__tela.mostra_mensagem(
                f"Serviço adicionado. Total: R$ {reserva.valor_total:.2f}"
            )

        except (ReservaException, ValidacaoException) as e:
            self.__tela.mostra_mensagem(str(e))


    def adicionar_pet_reserva(self):
        try:
            reserva = self.selecionar_reserva()
            if not reserva:
                return

            dados = self.__tela.pega_dados_pet()
            if not dados:
                raise ValidacaoException("Operação cancelada.")

            pet = Pet(nome_pet=dados["nome_pet"], especie=dados["especie"])
            reserva.adicionar_pet(pet)

            self.__tela.mostra_mensagem(
                f"Pet adicionado. Total: R$ {reserva.valor_total:.2f}"
            )

        except (ReservaException, ValidacaoException) as e:
            self.__tela.mostra_mensagem(str(e))


    def mostrar_valor_total_reserva(self):
        reserva = self.selecionar_reserva()
        if reserva:
            self.__tela.mostra_valor_total(reserva.id, reserva.valor_total)


    def gerar_relatorio_hospede(self):
        try:
            cpf = self.__tela.pega_cpf_hospede_relatorio()
            hosp = self.__controlador_hospede.busca_hospede(cpf)

            if not hosp:
                raise ReservaException("Hóspede não encontrado.")

            reservas = [
                r.get_all_data()
                for r in self.__reservas
                if any(h.cpf == cpf for h in r.hospedes)
            ]

            self.__tela.mostra_relatorio_hospede(cpf, reservas)

        except (ReservaException, ValidacaoException) as e:
            self.__tela.mostra_mensagem(str(e))

    def gerar_relatorio_tipo_servico(self):
        try:
            tipo = self.__tela.pega_tipo_servico_relatorio()
            if not tipo:
                raise ValidacaoException("Cancelado.")

            servicos = []
            for r in self.__reservas:
                for s in r.servicos_quarto:
                    if s.tipo_servico.lower() == tipo.lower():
                        servicos.append({
                            "reserva_id": r.id,
                            "tipo": s.tipo_servico,
                            "valor": s.valor,
                            "num_quarto": s.quarto.numero,
                            "funcionario_nome": s.funcionario.nome,
                            "funcionario_cpf": s.funcionario.cpf
                        })

            if not servicos:
                self.__tela.mostra_mensagem("Nenhum serviço encontrado.")
                return

            self.__tela.mostra_relatorio_servico(tipo, servicos)

        except (ReservaException, ValidacaoException) as e:
            self.__tela.mostra_mensagem(str(e))

    @property
    def reservas(self) -> List[Reserva]:
        return self.__reservas
