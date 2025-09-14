
from hospede import Hospede
from quarto import Quarto
from typing import List

class Reserva:
    def __init__(self, hospedes: List[Hospede], quartos: List[Quarto], data_checkin: str, data_checkout: str, valor_total: float, status: str):
        if not isinstance(hospedes, list):
            raise TypeError("hospedes deve ser uma lista de objetos Hospede")
        if not isinstance(quartos, list):
            raise TypeError("quartos deve ser uma lista de objetos Quarto")
        
        self.__hospedes = hospedes
        self.__quartos = quartos
        self.__data_checkin = data_checkin
        self.__data_checkout = data_checkout
        self.__valor_total = valor_total
        self.__status = status

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
    def valor_total(self):
        return self.__valor_total

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status: str):
        self.__status = status

    def verifica_hospede(self) -> bool:
        return any(h.is_adulto() for h in self.__hospedes)

    def fazer_reserva(self):
        for quarto in self.__quartos:
            if not quarto.disponibilidade:
                print(f"Quarto {quarto.numero} está ocupado. Reserva não concluída.")
                return
        for quarto in self.__quartos:
            quarto.reservar_quarto()
        
        self.__status = "confirmada"
        self.calcular_valor_total()
        print("Reserva realizada com sucesso.")

    def cancelar_reserva(self):
        for quarto in self.__quartos:
            quarto.liberar_quarto()
        self.__status = "cancelada"
        print("Reserva cancelada.")

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
        print("Reserva editada com sucesso.")

    def calcular_valor_total(self):
        dias = self.__calcular_dias()
        total = 0.0
        for quarto in self.__quartos:
            adultos = sum(1 for h in self.__hospedes if h.is_adulto())
            criancas = sum(1 for h in self.__hospedes if h.is_crianca())
            valor_por_adulto = quarto.valor_diaria
            total += adultos * valor_por_adulto * dias
        self.__valor_total = total
        print(f"Valor total da reserva: R$ {self.__valor_total:.2f}")

    def __calcular_dias(self) -> int:
        from datetime import datetime
        formato = "%d/%m/%Y"
        checkin = datetime.strptime(self.__data_checkin, formato)
        checkout = datetime.strptime(self.__data_checkout, formato)
        return (checkout - checkin).days
