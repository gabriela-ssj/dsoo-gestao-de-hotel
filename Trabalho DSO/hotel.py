from hospede import Hospede
from funcionario import Funcionario
from quarto import Quarto
from reserva import Reserva
from recursos_humanos import Rh

class Hotel:
    def __init__(self, nome:str, hospedes:Hospede, funcionarios:Funcionario, quartos:Quarto, reservas:Reserva, recursos_humanos:Rh):
        if not isinstance(nome, str):
            self.__nome = str(nome)
        else:
            self.__nome = nome
        self.__hospedes = hospedes
        self.__funcionarios = Funcionario[]
        self.__quartos = []
        self.__reservas = []
        self.__recursos_humanos = recursos_humanos
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome:str):
        self.__nome = nome

    @property
    def recursos_humanos(self):
        return self.__recusros_humanos