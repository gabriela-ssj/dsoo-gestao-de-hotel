from funcionario import Funcionario

class Rh:
    def __init__(self, funcionarios: Funcionario):
        self.__funcionarios = funcionarios

    @property
    def funcionarios(self):
        return self.__funcionarios

    @funcionarios.setter
    def funcionarios(self, funcionarios):
        self.__funcionarios = funcionarios
