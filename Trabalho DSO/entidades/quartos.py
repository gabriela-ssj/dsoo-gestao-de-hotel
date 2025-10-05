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

    def adicionar_pet(self, pet: Pet):
        total_pets = sum(p.quant_pet for p in self.pets)
        if total_pets + pet.quant_pet > 2:
            print(f"⚠️ Suite {self.numero} aceita no máximo 2 pets.")
        else:
            super().adicionar_pet(pet)

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) > self.capacidade_pessoas:
            print(f"Suite {self.numero} excede capacidade de 4 pessoas.")
            return False

        adultos = sum(1 for h in hospedes if h.is_adulto())
        criancas = sum(1 for h in hospedes if h.is_crianca())

        if adultos > 2 or criancas > 2:
            print(f"Suite {self.numero} permite no máximo 2 adultos e 2 crianças.")
            return False

        self._Quarto__hospedes = hospedes
        print(f"{len(hospedes)} hóspedes alocados na Suite {self.numero}.")
        return True

class Duplo(Quarto):
    def __init__(self, numero: int, valor_diaria: float, disponibilidade: bool):
        super().__init__(numero, valor_diaria, disponibilidade, capacidade_pessoas=2)

    def adicionar_pet(self, pet: Pet):
        if pet.especie.lower() not in ["cachorro", "gato"]:
            print(f"⚠️ Quarto Duplo {self.numero} só aceita cachorro ou gato.")
        elif len(self.pets) >= 1:
            print(f"⚠️ Quarto Duplo {self.numero} aceita apenas 1 pet.")
        else:
            super().adicionar_pet(pet)

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) > self.capacidade_pessoas:
            print(f"Quarto Duplo {self.numero} excede capacidade de 2 pessoas.")
            return False

        adultos = sum(1 for h in hospedes if h.is_adulto())
        criancas = sum(1 for h in hospedes if h.is_crianca())

        if adultos == 2 or (adultos == 1 and criancas == 1):
            self._Quarto__hospedes = hospedes
            print(f"{len(hospedes)} hóspedes alocados no Quarto Duplo {self.numero}.")
            return True

        print(f"Quarto Duplo {self.numero} permite 2 adultos ou 1 adulto + 1 criança.")
        return False

class Simples(Quarto):
    def __init__(self, numero: int, valor_diaria: float, disponibilidade: bool):
        super().__init__(numero, valor_diaria, disponibilidade, capacidade_pessoas=1)

    def adicionar_pet(self, pet: Pet):
        print(f"⚠️ Quarto Simples {self.numero} não aceita pets.")

    def alocar_hospedes(self, hospedes: List[Hospede]) -> bool:
        if len(hospedes) != 1:
            print(f"Quarto Simples {self.numero} aceita apenas 1 hóspede.")
            return False

        hospede = hospedes[0]
        if hospede.is_crianca():
            print(f"Quarto Simples {self.numero} não aceita crianças.")
            return False

        self._Quarto__hospedes = hospedes
        print(f"Hóspede adulto alocado no Quarto Simples {self.numero}.")
        return True
