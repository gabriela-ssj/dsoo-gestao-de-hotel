from funcionario import Funcionario  
from typing import List

class Rh:
    def __init__(self, funcionarios: List[Funcionario] = None):
        self.__funcionarios = funcionarios if funcionarios is not None else []

    @property
    def funcionarios(self):
        return self.__funcionarios

    @funcionarios.setter
    def funcionarios(self, funcionarios: List[Funcionario]):
        self.__funcionarios = funcionarios

    def incluir_funcionario(self, funcionario: Funcionario):
        self.__funcionarios.append(funcionario)

    def excluir_funcionario(self, cpf: str):
        self.__funcionarios = [f for f in self.__funcionarios if f.cpf != cpf]

    def alterar_funcionario(self, cpf: str, dados: dict):
        for f in self.__funcionarios:
            if f.cpf == cpf:
                for chave, valor in dados.items():
                    if hasattr(f, chave):
                        setattr(f, chave, valor)

    def listar_funcionarios(self) -> List[str]:
        return [
            f"{func.nome} - {func.cargo.tipo_cargo} - R$ {func.cargo.salario_base:.2f}"
            for func in self.__funcionarios
        ]

    def realizar_pagamento(self, cpf: str, metodo: str) -> str:
        for f in self.__funcionarios:
            if f.cpf == cpf:
                cargo = f.cargo.tipo_cargo
                salario = f.cargo.salario_base
                bonus = f.cargo.calcular_bonus()
                total = salario + bonus
                return (
                    f"Pagamento realizado para {f.nome} ({cargo}) via {metodo}.\n"
                    f"Salário base: R$ {salario:.2f}\n"
                    f"Bônus: R$ {bonus:.2f}\n"
                    f"Total: R$ {total:.2f}"
                )
        return f"Funcionário com CPF {cpf} não encontrado."
