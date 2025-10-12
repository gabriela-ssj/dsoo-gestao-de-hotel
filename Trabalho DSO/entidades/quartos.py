from entidades.quarto import Quarto
from entidades.hospede import Hospede
from entidades.pet import Pet
from typing import List


class Suite(Quarto):
    def __init__(self, numero: int, valor_diaria: float, disponibilidade: bool, hidro: bool = False):
        super().__init__(numero, valor_diaria, disponibilidade, capacidade_pessoas=4)
        self.__hidro = hidro

    @property
    def hidro(self) -> bool:
        return self.__hidro

    @hidro.setter
    def hidro(self, hidro: bool):
        self.__hidro = hidro

    def adicionar_pet(self, pet: Pet) -> bool:
        return len(self.pets) < 2 and super().adicionar_pet(pet)

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) > self.capacidade_pessoas:
            return False
        adultos = sum(h.is_adulto() for h in hospedes)
        criancas = sum(h.is_crianca() for h in hospedes)
        return adultos <= 2 and criancas <= 2 and super().alocar_hospedes(hospedes)


class Duplo(Quarto):
    def __init__(self, numero: int, valor_diaria: float, disponibilidade: bool):
        super().__init__(numero, valor_diaria, disponibilidade, capacidade_pessoas=2)

    def adicionar_pet(self, pet: Pet) -> bool:
        if pet.especie.lower() not in ["cachorro", "gato"]:
            return False
        return len(self.pets) < 1 and super().adicionar_pet(pet)

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) > self.capacidade_pessoas:
            return False
        adultos = sum(h.is_adulto() for h in hospedes)
        criancas = sum(h.is_crianca() for h in hospedes)
        return (adultos == 2 or (adultos == 1 and criancas == 1)) and super().alocar_hospedes(hospedes)


class Simples(Quarto):
    def __init__(self, numero: int, valor_diaria: float, disponibilidade: bool):
        super().__init__(numero, valor_diaria, disponibilidade, capacidade_pessoas=1)

    def adicionar_pet(self, pet: Pet) -> bool:
        return False

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) != 1:
            return False
        return not hospedes[0].is_crianca() and super().alocar_hospedes(hospedes)
