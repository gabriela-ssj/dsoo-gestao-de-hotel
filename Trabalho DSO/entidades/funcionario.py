from entidades.pessoa import Pessoa
from entidades.cargo import Cargo

class Funcionario(Pessoa):
    def __init__(self, nome: str, cpf: str, telefone: str, idade: int, email: str, cargo: Cargo):
        super().__init__(nome=nome, cpf=cpf, telefone=telefone, idade=idade, email=email)
        self._cargo = cargo
        self._salario_base = cargo.salario_base  

    @property
    def cargo(self) -> Cargo:
        return self._cargo

    @cargo.setter
    def cargo(self, novo_cargo: Cargo):
        self._cargo = novo_cargo
        self._salario_base = novo_cargo.salario_base  

    @property
    def salario_base(self) -> float:
        return self._salario_base

    def registrar_servico(self) -> str:
        return f"{self.nome} registrou um serviço como {self.cargo.nome}."

    def exibir_dados(self) -> str:
        return (
            f"Nome: {self.nome}\n"
            f"CPF: {self.cpf}\n"
            f"Telefone: {self.telefone}\n"
            f"Idade: {self.idade}\n"
            f"Email: {self.email}\n"
            f"Cargo: {self.cargo.nome}\n"
            f"Salário Base: R$ {self.salario_base:.2f}"
        )
