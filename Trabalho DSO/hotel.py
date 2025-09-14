from hospede import Hospede
from funcionario import Funcionario
from quarto import Quarto
from reserva import Reserva
from recursos_humanos import Rh
from typing import List

class Hotel:
    def __init__(self, nome:str, hospedes:Hospede, funcionarios:Funcionario, quartos:Quarto, reservas:Reserva, recursos_humanos:Rh):
        if not isinstance(nome, str):
            raise TypeError("O nome do hotel deve ser uma string")
        
        self.__nome = nome
        self.__hospedes = list[Hospede] = []
        self.__funcionarios = list[Funcionario] = []
        self.__quartos = list[Quarto] = []
        self.__reservas = list [Reserva] = []
        self.__recursos_humanos = recursos_humanos

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome:str):
        if not isinstance(nome, str):
            raise TypeError("O nome do hotel deve ser uma string")
        self.__nome = nome

    @property
    def recursos_humanos(self):
        return self.__recursos_humanos

    def adicionar_hospede(self, hospede: Hospede):
        self.__hospedes.append(hospede)

    def adicionar_funcionario(self, funcionario: Funcionario):
        self.__funcionarios.append(funcionario)

    def adicionar_quarto(self, quarto: Quarto):
        self.__quartos.append(quarto)

    def adicionar_reserva(self, reserva: Reserva):
        self.__reservas.append(reserva)

    def buscar_quarto(self):
        pass