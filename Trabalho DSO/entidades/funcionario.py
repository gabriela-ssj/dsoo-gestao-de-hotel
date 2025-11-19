from entidades.cargo import Cargo
from entidades.pessoa import Pessoa
from typing import Optional, Dict, Any

class Funcionario(Pessoa):
    def __init__(self, cpf: str, nome: str, idade: int, telefone: str, email: str, cargo: Cargo, salario: float):
        super().__init__(cpf, nome, idade, telefone, email)

        if not isinstance(cargo, Cargo):
            raise TypeError("Cargo deve ser um objeto da classe Cargo.")
        if not isinstance(salario, (int, float)) or salario < 0:
            raise ValueError("Salário deve ser um número positivo.")

        self._cargo = cargo
        self._salario = float(salario)

    @property
    def cargo(self) -> Cargo:
        return self._cargo

    @cargo.setter
    def cargo(self, cargo: Cargo):
        if not isinstance(cargo, Cargo):
            raise TypeError("Cargo deve ser um objeto da classe Cargo.")
        self._cargo = cargo

    @property
    def salario(self) -> float:
        return self._salario

    @salario.setter
    def salario(self, valor: float):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("Salário deve ser um número positivo.")
        self._salario = float(valor)

    def __str__(self) -> str:
        return (f"{super().__str__()}, Cargo: {self.cargo.tipo_cargo.capitalize()}, "
                f"Salário: R\${self.salario:.2f}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cpf": self.cpf,
            "nome": self.nome,
            "idade": self.idade,
            "telefone": self.telefone,
            "email": self.email,
            "tipo_cargo": self.cargo.tipo_cargo if self.cargo else None, 
            "salario": self.salario
        }
