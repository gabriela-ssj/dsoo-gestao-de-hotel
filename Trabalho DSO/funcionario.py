
from pessoa import Pessoa

class Funcionario(Pessoa):
    def __init__(self, cpf:str, nome:str, idade:int, telefone:str, email:str, cargo: str, salario: float):
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
    
    def registrar_servico(self):
        pass