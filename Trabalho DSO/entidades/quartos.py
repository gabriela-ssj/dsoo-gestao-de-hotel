from entidades.quarto import Quarto
from entidades.hospede import Hospede
from entidades.pet import Pet
from typing import List

class Suite(Quarto):
    def __init__(self, numero: int, valor_diaria: float, disponibilidade: bool, hidro: bool = False):
        numero_formatado = f"S{numero}"
        super().__init__(numero_formatado, valor_diaria, disponibilidade, capacidade_pessoas=4)
        self.__hidro = hidro
        self.__pets: List[Pet] = []

    @property
    def hidro(self) -> bool:
        return self.__hidro

    @hidro.setter
    def hidro(self, hidro: bool):
        self.__hidro = hidro

    @property
    def pets(self) -> List[Pet]:
        return self.__pets.copy()

    def adicionar_pet(self, pet: Pet) -> bool:
        total_pets = sum(p.quant_pet for p in self.__pets)
        if total_pets + pet.quant_pet > 2:
            return False
        self.__pets.append(pet)
        return True

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) > self.capacidade_pessoas:
            return False
        adultos = sum(h.is_adulto() for h in hospedes)
        criancas = sum(h.is_crianca() for h in hospedes)
        if adultos > 2 or criancas > 2:
            return False
        self._Quarto__hospedes = hospedes
        return True


class Duplo(Quarto):
    def __init__(self, numero: int, valor_diaria: float, disponibilidade: bool):
        numero_formatado = f"D{numero}"
        super().__init__(numero_formatado, valor_diaria, disponibilidade, capacidade_pessoas=2)
        self.__pets: List[Pet] = []

    @property
    def pets(self) -> List[Pet]:
        return self.__pets.copy()

    def adicionar_pet(self, pet: Pet) -> bool:
        if pet.especie.lower() not in ["cachorro", "gato"]:
            return False
        if len(self.__pets) >= 1:
            return False
        self.__pets.append(pet)
        return True

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) > self.capacidade_pessoas:
            return False
        adultos = sum(h.is_adulto() for h in hospedes)
        criancas = sum(h.is_crianca() for h in hospedes)
        if adultos == 2 or (adultos == 1 and criancas == 1):
            self._Quarto__hospedes = hospedes
            return True
        return False


class Simples(Quarto):
    def __init__(self, numero: int, valor_diaria: float, disponibilidade: bool):
        numero_formatado = f"Q{numero}"
        super().__init__(numero_formatado, valor_diaria, disponibilidade, capacidade_pessoas=1)

    def adicionar_pet(self, pet: Pet) -> bool:
        return False  

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) != 1:
            return False
        hospede = hospedes[0]
        if hospede.is_crianca():
            return False
        self._Quarto__hospedes = hospedes
        return True
