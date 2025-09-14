
from quarto import Quarto

class Suite(Quarto):
    def __init__(self, numero:int, valor_diaria:float, disponibilidade:bool, capacidade_pessoas:int, hidro:bool):
        super().__init__(numero, valor_diaria, disponibilidade, capacidade_pessoas)
        self.__hidro = hidro
    
    @property
    def hidro(self):
        return self.__hidro
    
    @hidro.setter
    def hidro(self, hidro):
        self.__hidro = hidro

class Duplo(Quarto):
    def __init__(self, numero:int, valor_diaria:float, disponibilidade:bool, capacidade_pessoas:int):
        super().__init__(numero, valor_diaria, disponibilidade, capacidade_pessoas)

class Simples(Quarto):
    def __init__(self, numero:int, valor_diaria:float, disponibilidade:bool, capacidade_pessoas:int):
        super().__init__(numero, valor_diaria, disponibilidade, capacidade_pessoas)