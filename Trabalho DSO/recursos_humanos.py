
from funcionario import Funcionario
from typing import List

class Rh:
    def __init__(self, funcionarios: List[Funcionario] = []):
        self.__funcionarios = funcionarios

    @property
    def funcionarios(self):
        return self.__funcionarios

    @funcionarios.setter
    def funcionarios(self, funcionarios):
        self.__funcionarios = funcionarios

    def incluir_funcionario(self, funcionario: Funcionario):
        self.__funcionarios.append(funcionario)

    def excluir_funcionario(self, funcionario: Funcionario):
        if funcionario in self.__funcionarios:
            self.__funcionarios.remove(funcionario)

    def listar_funcionarios(self):
        return self.__funcionarios
