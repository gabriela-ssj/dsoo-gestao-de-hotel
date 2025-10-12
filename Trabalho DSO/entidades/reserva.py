from entidades.hospede import Hospede
from entidades.quarto import Quarto
from entidades.servico_de_quarto import ServicoDeQuarto
from entidades.pet import Pet
from typing import List, Optional
from datetime import datetime

class Reserva:
    def __init__(
        self,
        hospedes: List[Hospede],
        quartos: List[Quarto],
        data_checkin: str,
        data_checkout: str,
        status: str,
        pets: Optional[List[Pet]] = None
    ):
        self.__hospedes = hospedes
        self.__quartos = quartos
        self.__data_checkin = data_checkin
        self.__data_checkout = data_checkout
        self.__status = status
        self.__valor_total = 0.0
        self.__servicos_quarto: List[ServicoDeQuarto] = []
        self.__pets: List[Pet] = pets if pets else []

    @property
    def hospedes(self) -> List[Hospede]:
        return self.__hospedes.copy()

    @property
    def quartos(self) -> List[Quarto]:
        return self.__quartos.copy()

    @property
    def data_checkin(self) -> str:
        return self.__data_checkin

    @property
    def data_checkout(self) -> str:
        return self.__data_checkout

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, novo_status: str):
        self.__status = novo_status

    @property
    def valor_total(self) -> float:
        return self.__valor_total

    @property
    def servicos_quarto(self) -> List[ServicoDeQuarto]:
        return self.__servicos_quarto.copy()

    @property
    def pets(self) -> List[Pet]:
        return self.__pets.copy()

    def adicionar_servico_quarto(self, servico: ServicoDeQuarto) -> None:
        self.__servicos_quarto.append(servico)

    def adicionar_pet(self, pet: Pet) -> None:
        self.__pets.append(pet)
        for quarto in self.__quartos:
            quarto.adicionar_pet(pet)

    def reservar_quartos(self) -> None:
        for quarto in self.__quartos:
            quarto.reservar_quarto()

    def liberar_quartos(self) -> None:
        for quarto in self.__quartos:
            quarto.liberar_quarto()

    def editar_reserva(
        self,
        nova_data_checkin: Optional[str] = None,
        nova_data_checkout: Optional[str] = None,
        novo_quarto: Optional[List[Quarto]] = None
    ) -> None:
        if nova_data_checkin:
            self.__data_checkin = nova_data_checkin
        if nova_data_checkout:
            self.__data_checkout = nova_data_checkout
        if novo_quarto:
            self.liberar_quartos()
            self.__quartos = novo_quarto
            self.reservar_quartos()

    def calcular_valor_total(self) -> None:
        dias = self.__calcular_dias()
        total = 0.0
        for quarto in self.__quartos:
            for hospede in self.__hospedes:
                if hospede.is_adulto():
                    total += quarto.valor_diaria * dias
        total += sum(servico.valor for servico in self.__servicos_quarto)
        total += sum(pet.calcular_taxa_pet(50.0) for pet in self.__pets)
        self.__valor_total = total

    def __calcular_dias(self) -> int:
        formato = "%d/%m/%Y"
        try:
            checkin = datetime.strptime(self.__data_checkin, formato)
            checkout = datetime.strptime(self.__data_checkout, formato)
            dias = (checkout - checkin).days
            if dias <= 0:
                raise ValueError("Data de check-out deve ser posterior ao check-in.")
            return dias
        except ValueError as e:
            raise ValueError(f"Erro ao calcular dias da reserva: {e}")
