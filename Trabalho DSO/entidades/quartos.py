# entidades\quartos.py
from entidades.quarto import Quarto
from entidades.hospede import Hospede
from entidades.pet import Pet
from typing import List


class Suite(Quarto):
    def __init__(self, numero: int, valor_diaria: float, disponibilidade: bool, hidro: bool = False):
        super().__init__(numero, valor_diaria, disponibilidade, capacidade_pessoas=4)
        self.__hidro = hidro

    @property
    def hidro(self):
        return self.__hidro

    @hidro.setter
    def hidro(self, hidro: bool):
        self.__hidro = hidro

    def adicionar_pet(self, pet: Pet) -> bool:
        total_pets = len(self.pets)
        if total_pets + 1 > 2:
            print(f"⚠️ Suite {self.numero} aceita no máximo 2 pets.")
            return False
        return super().adicionar_pet(pet)

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) > self.capacidade_pessoas:
            print(f"Suite {self.numero} excede capacidade de 4 pessoas.")
            return False

        adultos = sum(1 for h in hospedes if h.is_adulto())
        criancas = sum(1 for h in hospedes if h.is_crianca())

        if adultos > 2 or criancas > 2:
            print(f"Suite {self.numero} permite no máximo 2 adultos e 2 crianças.")
            return False

        return super().alocar_hospedes(hospedes)


class Duplo(Quarto):
    def __init__(self, numero: int, valor_diaria: float, disponibilidade: bool):
        super().__init__(numero, valor_diaria, disponibilidade, capacidade_pessoas=2)

    def adicionar_pet(self, pet: Pet) -> bool:
        if pet.especie.lower() not in ["cachorro", "gato"]:
            print(f"⚠️ Quarto Duplo {self.numero} só aceita cachorro ou gato.")
            return False

        current_pet_count = len(self.pets)
        if current_pet_count + 1 > 1:
            print(f"⚠️ Quarto Duplo {self.numero} aceita apenas 1 pet.")
        return super().adicionar_pet(pet)  # Chama o método da classe base

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) > self.capacidade_pessoas:
            print(f"Quarto Duplo {self.numero} excede capacidade de 2 pessoas.")
            return False

        adultos = sum(1 for h in hospedes if h.is_adulto())
        criancas = sum(1 for h in hospedes if h.is_crianca())

        if adultos == 2 or (adultos == 1 and criancas == 1):
            return super().alocar_hospedes(hospedes)
        return False


class Simples(Quarto):
    def __init__(self, numero: int, valor_diaria: float, disponibilidade: bool):
        super().__init__(numero, valor_diaria, disponibilidade, capacidade_pessoas=1)

    def adicionar_pet(self, pet: Pet) -> bool:
        print(f"⚠️ Quarto Simples {self.numero} não aceita pets.")
        return False

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) != 1:
            print(f"Quarto Simples {self.numero} aceita apenas 1 hóspede.")
            return False

        hospede = hospedes[0]
        if hospede.is_crianca():
            print(f"Quarto Simples {self.numero} não aceita crianças.")
            return False

        return super().alocar_hospedes(hospedes)