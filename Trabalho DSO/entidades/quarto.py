from abc import ABC, abstractmethod
from entidades.hospede import Hospede
from typing import List, Tuple

class Quarto(ABC):
    @abstractmethod
    def __init__(self, numero: int, valor_diaria: float, disponibilidade: bool, capacidade_pessoas: int):
        self.__numero = numero
        self.__valor_diaria = valor_diaria
        self.__disponibilidade = disponibilidade
        self.__capacidade_pessoas = capacidade_pessoas
        self.__hospedes: List[Hospede] = []

    @property
    def numero(self) -> int:
        return self.__numero

    @numero.setter
    def numero(self, numero: int):
        self.__numero = numero

    @property
    def valor_diaria(self) -> float:
        return self.__valor_diaria

    @valor_diaria.setter
    def valor_diaria(self, valor_diaria: float):
        self.__valor_diaria = valor_diaria

    @property
    def disponibilidade(self) -> bool:
        return self.__disponibilidade

    @disponibilidade.setter
    def disponibilidade(self, disponibilidade: bool):
        self.__disponibilidade = disponibilidade

    @property
    def capacidade_pessoas(self) -> int:
        return self.__capacidade_pessoas

    @capacidade_pessoas.setter
    def capacidade_pessoas(self, capacidade_pessoas: int):
        self.__capacidade_pessoas = capacidade_pessoas

    @property
    def hospedes(self) -> List[Hospede]:
        return self.__hospedes

    def reservar_quarto(self):
        self.__disponibilidade = False

    def liberar_quarto(self):
        self.__disponibilidade = True
        self.__hospedes.clear()

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) > self.__capacidade_pessoas:
            return False
        self.__hospedes = hospedes
        return True

    def contador_adultos_criancas(self) -> Tuple[int, int]:
        adultos = sum(1 for h in self.__hospedes if h.is_adulto())
        criancas = sum(1 for h in self.__hospedes if h.is_crianca())
        return adultos, criancas
