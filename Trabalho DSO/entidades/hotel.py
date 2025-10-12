from entidades.hospede import Hospede
from entidades.quarto import Quarto
from entidades.reserva import Reserva
from entidades.recursos_humanos import Rh
from typing import List, Optional

class Hotel:
    def __init__(
        self,
        nome: str,
        hospedes: Optional[List[Hospede]] = None,
        quartos: Optional[List[Quarto]] = None,
        reservas: Optional[List[Reserva]] = None,
        recursos_humanos: Optional[Rh] = None
    ):
        if not isinstance(nome, str):
            raise TypeError("O nome do hotel deve ser uma string")

        self.__nome = nome
        self.__hospedes: List[Hospede] = hospedes if hospedes is not None else []
        self.__quartos: List[Quarto] = quartos if quartos is not None else []
        self.__reservas: List[Reserva] = reservas if reservas is not None else []
        self.recursos_humanos: Rh = recursos_humanos if recursos_humanos else Rh()

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("O nome do hotel deve ser uma string")
        self.__nome = nome

    @property
    def hospedes(self) -> List[Hospede]:
        return self.__hospedes.copy()

    @property
    def quartos(self) -> List[Quarto]:
        return self.__quartos.copy()

    @property
    def reservas(self) -> List[Reserva]:
        return self.__reservas.copy()

    def adicionar_hospede(self, hospede: Hospede) -> None:
        if not any(h.cpf == hospede.cpf for h in self.__hospedes):
            self.__hospedes.append(hospede)

    def excluir_hospede(self, cpf: str) -> bool:
        original_len = len(self.__hospedes)
        self.__hospedes = [h for h in self.__hospedes if h.cpf != cpf]
        return len(self.__hospedes) < original_len

    def adicionar_quarto(self, quarto: Quarto) -> None:
        if not any(q.numero == quarto.numero for q in self.__quartos):
            self.__quartos.append(quarto)

    def excluir_quarto(self, numero: int) -> bool:
        original_len = len(self.__quartos)
        self.__quartos = [q for q in self.__quartos if q.numero != numero]
        return len(self.__quartos) < original_len

    def alterar_quarto(self, numero: int, novos_dados: dict) -> bool:
        for quarto in self.__quartos:
            if quarto.numero == numero:
                for chave, valor in novos_dados.items():
                    if hasattr(quarto, chave):
                        setattr(quarto, chave, valor)
                return True
        return False

    def adicionar_reserva(self, reserva: Reserva) -> None:
        self.__reservas.append(reserva)
