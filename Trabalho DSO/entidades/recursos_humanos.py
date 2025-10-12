from entidades.funcionario import Funcionario
from typing import List

class Rh:
    def __init__(self, funcionarios: List[Funcionario] = None):
        self.__funcionarios = funcionarios if funcionarios is not None else []

    @property
    def funcionarios(self) -> List[Funcionario]:
        return self.__funcionarios

    @funcionarios.setter
    def funcionarios(self, funcionarios: List[Funcionario]):
        self.__funcionarios = funcionarios

    def adicionar_funcionario(self, funcionario: Funcionario):
        self.__funcionarios.append(funcionario)

    def excluir_funcionario(self, cpf: str):
        self.__funcionarios = [f for f in self.__funcionarios if f.cpf != cpf]

    def alterar_funcionario(self, cpf: str, dados: dict):
        for f in self.__funcionarios:
            if f.cpf == cpf:
                for chave, valor in dados.items():
                    if hasattr(f, chave):
                        setattr(f, chave, valor)

    def buscar_funcionario(self, cpf: str) -> Funcionario | None:
        for f in self.__funcionarios:
            if f.cpf == cpf:
                return f
        return None
