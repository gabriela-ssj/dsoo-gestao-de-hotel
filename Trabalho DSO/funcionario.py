from pessoa import Pessoa
from pessoa import cpf
from pessoa import nome
from pessoa import idade
from pessoa import telefone
from pessoa import email

class Funcionario(Pessoa):
    def __init__(self, cargo: str, salario: float):
        super().__init__(cpf, nome, idade, telefone, email)
        self.__cargo = cargo
        self.__salario = salario

    @property
    def cargo(self):
        return self.__cargo

    @cargo.setter
    def cargo(self, cargo):
        self.__cargo = cargo

    @property
    def salario(self):
        return self.__salario

    @salario.setter
    def salario(self, salario):
        self.__salario = salario 
    