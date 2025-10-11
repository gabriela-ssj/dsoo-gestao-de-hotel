from entidades.reserva import Reserva
from controlers.controlador_servicodequarto import ControladorServicoDeQuarto
from telas.tela_reserva import TelaReserva
from datetime import datetime

class ControladorReserva:
    def __init__(self, controlador_hospede, controlador_quarto, controlador_pet, controlador_funcionario):
        self.__reservas: list[Reserva] = []
        self.__tela = TelaReserva()
        self.__controlador_hospede = controlador_hospede
        self.__controlador_quarto = controlador_quarto
        self.__controlador_pet = controlador_pet
        self.__controlador_funcionario = controlador_funcionario
        self.__retorno_callback = None  

    def set_retorno_callback(self, callback):
        self.__retorno_callback = callback

    def fazer_reserva(self):
        try:
            self.__controlador_hospede.listar_hospedes_via_tela()
            cpfs = self.__tela.le_string("CPFs dos hóspedes (separados por vírgula): ").split(",")
            hospedes = []
            for cpf in cpfs:
                hospede = self.__controlador_hospede.busca_hospede(cpf.strip())
                if not hospede:
                    self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf.strip()} não encontrado.")
                    return
                hospedes.append(hospede)

            self.__controlador_quarto.listar_quartos()
            numeros = self.__tela.le_string("Números dos quartos (separados por vírgula): ").split(",")
            quartos = []
            for numero in numeros:
                quarto = self.__controlador_quarto.buscar_quarto(numero.strip())
                if not quarto or not quarto.disponibilidade:
                    self.__tela.mostra_mensagem(f"Quarto {numero.strip()} não encontrado ou indisponível.")
                    return
                quartos.append(quarto)

            checkin = self.__tela.le_string("Data de check-in (dd/mm/yyyy): ")
            checkout = self.__tela.le_string("Data de check-out (dd/mm/yyyy): ")
            formato = "%d/%m/%Y"
            dt_checkin = datetime.strptime(checkin, formato)
            dt_checkout = datetime.strptime(checkout, formato)
            if dt_checkout <= dt_checkin:
                raise ValueError("Check-out deve ser posterior ao check-in.")

            reserva = Reserva(hospedes, quartos, checkin, checkout, "ativa")
            reserva.reservar_quartos()

            if self.__tela.le_string("Deseja adicionar serviço de quarto? (s/n): ").lower() == "s":
                controlador_servico = ControladorServicoDeQuarto(self.__controlador_quarto, self.__controlador_funcionario)
                controlador_servico.solicitar_servico()
                if controlador_servico._ControladorServicoDeQuarto__servicos:
                    servico = controlador_servico._ControladorServicoDeQuarto__servicos[-1]
                    reserva.adicionar_servico_quarto(servico)

            self.__reservas.append(reserva)
            self.__tela.mostra_mensagem("✅ Reserva realizada com sucesso.")
        except ValueError as e:
            self.__tela.mostra_mensagem(f"⚠️ Erro: {e}")

    def cancelar_reserva(self):
        self.listar_reservas()
        index = self.__tela.le_num_inteiro("Número da reserva para cancelar: ")
        if 0 <= index < len(self.__reservas):
            reserva = self.__reservas[index]
            reserva.status = "cancelada"
            reserva.liberar_quartos()
            self.__tela.mostra_mensagem("✅ Reserva cancelada.")
        else:
            self.__tela.mostra_mensagem("⚠️ Reserva não encontrada.")

    def editar_reserva(self):
        self.listar_reservas()
        index = self.__tela.le_num_inteiro("Número da reserva para editar: ")
        if 0 <= index < len(self.__reservas):
            dados = self.__tela.pega_dados_edicao()
            reserva = self.__reservas[index]
            reserva.editar_reserva(
                nova_data_checkin=dados.get("checkin"),
                nova_data_checkout=dados.get("checkout"),
                novo_quarto=dados.get("quartos")
            )
            self.__tela.mostra_mensagem("✅ Reserva editada.")
        else:
            self.__tela.mostra_mensagem("⚠️ Reserva não encontrada.")

    def adicionar_servico(self):
        self.listar_reservas()
        index = self.__tela.le_num_inteiro("Número da reserva para adicionar serviço: ")
        if 0 <= index < len(self.__reservas):
            controlador_servico = ControladorServicoDeQuarto(self.__controlador_quarto, self.__controlador_funcionario)
            controlador_servico.solicitar_servico()
            if controlador_servico._ControladorServicoDeQuarto__servicos:
                servico = controlador_servico._ControladorServicoDeQuarto__servicos[-1]
                self.__reservas[index].adicionar_servico_quarto(servico)
                self.__tela.mostra_mensagem("✅ Serviço adicionado à reserva.")
        else:
            self.__tela.mostra_mensagem("⚠️ Reserva não encontrada.")

    def adicionar_pet(self):
        self.listar_reservas()
        index = self.__tela.le_num_inteiro("Número da reserva para adicionar pet: ")
        if 0 <= index < len(self.__reservas):
            self.__controlador_pet.listar_pets()
            nome_pet = self.__tela.le_string("Nome do pet a adicionar: ")
            pet = next((p for p in self.__controlador_pet.pets if p.nome_pet == nome_pet), None)
            if pet:
                self.__reservas[index].adicionar_pet(pet)
                self.__tela.mostra_mensagem("✅ Pet adicionado à reserva.")
            else:
                self.__tela.mostra_mensagem("⚠️ Pet não encontrado.")
        else:
            self.__tela.mostra_mensagem("⚠️ Reserva não encontrada.")

    def calcular_valor_total(self):
        self.listar_reservas()
        index = self.__tela.le_num_inteiro("Número da reserva para calcular valor: ")
        if 0 <= index < len(self.__reservas):
            try:
                self.__reservas[index].calcular_valor_total()
                valor = self.__reservas[index].valor_total
                self.__tela.mostra_mensagem(f"💰 Valor total da reserva: R${valor:.2f}")
            except ValueError as e:
                self.__tela.mostra_mensagem(f"⚠️ Erro: {e}")
        else:
            self.__tela.mostra_mensagem("⚠️ Reserva não encontrada.")

    def exibir_relatorio_por_hospede(self):
        relatorio = []
        for i, r in enumerate(self.__reservas):
            nomes = [h.nome for h in r.hospedes]
            relatorio.append(f"Reserva {i} | Hóspedes: {', '.join(nomes)} | Status: {r.status}")
        self.__tela.mostra_lista(relatorio)

    def exibir_relatorio_por_tipo_servico(self):
        relatorio = []
        for i, r in enumerate(self.__reservas):
            tipos = [s.tipo_servico for s in r.servicos_quarto]
            relatorio.append(f"Reserva {i} | Serviços: {', '.join(tipos) if tipos else 'Nenhum'}")
        self.__tela.mostra_lista(relatorio)

    def listar_reservas(self):
        if not self.__reservas:
            self.__tela.mostra_mensagem("Nenhuma reserva cadastrada.")
            return
        lista = [
            f"Reserva {i} | Check-in: {r.data_checkin} | Check-out: {r.data_checkout} | Status: {r.status} | Quartos: {[q.numero for q in r.quartos]}"
            for i, r in enumerate(self.__reservas)
        ]
        self.__tela.mostra_lista(lista)

    def retornar(self):
        if self.__retorno_callback:
            self.__retorno_callback()
        else:
            self.__tela.mostra_mensagem("Retornando ao menu anterior...")
