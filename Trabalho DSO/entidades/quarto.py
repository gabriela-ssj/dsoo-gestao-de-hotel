from abc import ABC, abstractmethod
from entidades.hospede import Hospede
from entidades.pet import Pet
from typing import List

class Quarto(ABC):

    @abstractmethod
    def __init__(self, numero: int, valor_diaria: float, disponibilidade: bool, capacidade_pessoas: int):
        self.__numero = numero
        self.__valor_diaria = valor_diaria
        self.__disponibilidade = disponibilidade
        self.__capacidade_pessoas = capacidade_pessoas
        self._hospedes: List[Hospede] = []
        self._pets: List[Pet] = []

    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, numero: int):
        self.__numero = numero

    @property
    def valor_diaria(self):
        return self.__valor_diaria

    @valor_diaria.setter
    def valor_diaria(self, valor_diaria: float):
        if not isinstance(valor_diaria, (int, float)) or valor_diaria <= 0:
            raise ValueError("Valor da diária deve ser um número positivo.")
        self.__valor_diaria = valor_diaria

    @property
    def disponibilidade(self):
        return self.__disponibilidade

    @disponibilidade.setter
    def disponibilidade(self, disponibilidade: bool):
        self.__disponibilidade = disponibilidade

    @property
    def capacidade_pessoas(self):
        return self.__capacidade_pessoas

    @capacidade_pessoas.setter
    def capacidade_pessoas(self, capacidade_pessoas: int):
        if not isinstance(capacidade_pessoas, int) or capacidade_pessoas <= 0:
            raise ValueError("Capacidade de pessoas deve ser um inteiro positivo.")
        self.__capacidade_pessoas = capacidade_pessoas

    @property
    def hospedes(self) -> List[Hospede]:
        return self._hospedes

    @property
    def pets(self) -> List[Pet]:
        return self._pets

    def reservar_quarto(self) -> bool:
        if self.__disponibilidade:
            self.__disponibilidade = False
            return True  # Sucesso na reserva
        return False  # Quarto já ocupado

    def liberar_quarto(self) -> bool:
        self.__disponibilidade = True
        self._hospedes.clear()
        self._pets.clear()
        return True

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) > self.__capacidade_pessoas:
            return False
        self._hospedes = hospedes
        return True

    def adicionar_pet(self, pet: Pet) -> bool:
        self._pets.append(pet)
        return True

    def listar_pets(self) -> List[str]:
        return [str(pet) for pet in self._pets]

    def contador_adultos_criancas(self) -> tuple[int, int]:
        adultos = sum(1 for hosp in self._hospedes if hosp.is_adulto())
        criancas = sum(1 for hosp in self._hospedes if hosp.is_crianca())
        return adultos, criancas

    def _set_hospedes(self, hospedes: List[Hospede]):
        self._hospedes = hospedes

    def _set_pets(self, pets: List[Pet]):
        self._pets = pets
