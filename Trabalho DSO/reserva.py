from hospede import Hospede
from quarto import Quarto
from servico_de_quarto import ServicoDeQuarto
from typing import List
from datetime import datetime

class Reserva:
    def __init__(self, hospedes: List[Hospede], quartos: List[Quarto], data_checkin: str, data_checkout: str, status: str):
        self.__hospedes = hospedes
        self.__quartos = quartos
        self.__data_checkin = data_checkin
        self.__data_checkout = data_checkout
        self.__status = status
        self.__valor_total = 0.0
        self.__servicos_quarto: List[ServicoDeQuarto] = []

    @property
    def hospedes(self):
        return self.__hospedes

    @property
    def quartos(self):
        return self.__quartos

    @property
    def data_checkin(self):
        return self.__data_checkin

    @property
    def data_checkout(self):
        return self.__data_checkout

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, novo_status: str):
        self.__status = novo_status

    @property
    def valor_total(self):
        return self.__valor_total

    @property
    def servicos_quarto(self):
        return self.__servicos_quarto

    def adicionar_servico_quarto(self, servico: ServicoDeQuarto):
        self.__servicos_quarto.append(servico)

    def fazer_reserva(self):
        try:
            formato = "%d/%m/%Y"
            checkin = datetime.strptime(self.__data_checkin, formato)
            checkout = datetime.strptime(self.__data_checkout, formato)
            if checkout <= checkin:
                print("⚠️ Data de check-out deve ser posterior à data de check-in.")
                return
        except ValueError:
            print("⚠️ Formato de data inválido. Use dd/mm/yyyy.")
            return

        for quarto in self.__quartos:
            if not quarto.disponibilidade:
                print(f"⚠️ Quarto {quarto.numero} está ocupado. Reserva não concluída.")
                return

        for quarto in self.__quartos:
            quarto.reservar_quarto()

        self.__status = "confirmada"
        self.calcular_valor_total()
        print("✅ Reserva realizada com sucesso.")

    def cancelar_reserva(self):
        for quarto in self.__quartos:
            quarto.liberar_quarto()
        self.__status = "cancelada"
        print("✅ Reserva cancelada.")

    def editar_reserva(self, nova_data_checkin: str = None, nova_data_checkout: str = None, novo_quarto: List[Quarto] = None):
        if nova_data_checkin:
            self.__data_checkin = nova_data_checkin
        if nova_data_checkout:
            self.__data_checkout = nova_data_checkout
        if novo_quarto:
            for quarto in self.__quartos:
                quarto.liberar_quarto()
            self.__quartos = novo_quarto
            for quarto in self.__quartos:
                quarto.reservar_quarto()
        print("✅ Reserva editada com sucesso.")

    def calcular_valor_total(self):
        dias = self.__calcular_dias()
        total = 0.0
        for quarto in self.__quartos:
            for hospede in self.__hospedes:
                if hospede.is_adulto():
                    total += quarto.valor_diaria * dias
        total += sum(servico.valor for servico in self.__servicos_quarto)
        self.__valor_total = total
        print(f"💰 Valor total da reserva: R$ {self.__valor_total:.2f}")

    def __calcular_dias(self) -> int:
        formato = "%d/%m/%Y"
        checkin = datetime.strptime(self.__data_checkin, formato)
        checkout = datetime.strptime(self.__data_checkout, formato)
        return (checkout - checkin).days

    def relatorio_por_hospede(self):
        relatorio = {}
        for hospede in self.__hospedes:
            nome = hospede.nome
            relatorio[nome] = []
            for servico in self.__servicos_quarto:
                if hospede in servico.quarto.hospedes:
                    relatorio[nome].append((servico.tipo_servico, servico.valor))
        return relatorio

    def relatorio_por_tipo_servico(self):
        resumo = {}
        for servico in self.__servicos_quarto:
            tipo = servico.tipo_servico
            resumo[tipo] = resumo.get(tipo, 0.0) + servico.valor
        return resumo
