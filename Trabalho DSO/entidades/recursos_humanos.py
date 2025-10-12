from entidades.funcionario import Funcionario
from typing import List, Optional

class Rh:
    def __init__(self, funcionarios: Optional[List[Funcionario]] = None):
        self.__funcionarios: List[Funcionario] = funcionarios if funcionarios is not None else []

    @property
    def funcionarios(self) -> List[Funcionario]:
        return self.__funcionarios.copy()

    @funcionarios.setter
    def funcionarios(self, funcionarios: List[Funcionario]):
        self.__funcionarios = funcionarios

    def adicionar_funcionario(self, funcionario: Funcionario) -> None:
        if not any(f.cpf == funcionario.cpf for f in self.__funcionarios):
            self.__funcionarios.append(funcionario)

    def excluir_funcionario(self, cpf: str) -> bool:
        original_len = len(self.__funcionarios)
        self.__funcionarios = [f for f in self.__funcionarios if f.cpf != cpf]
        return len(self.__funcionarios) < original_len

    def alterar_funcionario(self, cpf: str, dados: dict) -> bool:
        funcionario = self.buscar_funcionario(cpf)
        if funcionario:
            for chave, valor in dados.items():
                if hasattr(funcionario, chave):
                    setattr(funcionario, chave, valor)
            return True
        return False

    def buscar_funcionario(self, cpf: str) -> Optional[Funcionario]:
        return next((f for f in self.__funcionarios if f.cpf == cpf), None)
