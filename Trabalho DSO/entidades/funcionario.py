from entidades.pessoa import Pessoa
from entidades.cargo import Cargo

class Funcionario(Pessoa):
    def __init__(self, nome: str, cpf: str, telefone: str, idade: int, email: str, cargo: Cargo):
        super().__init__(nome=nome,cpf= cpf,telefone= telefone,idade= idade,email=email)
        self._cargo = cargo

    def _definir_salario_base(self, cargo):
        return tabela[cargo]

    @property
    def cargo(self):
        return self._cargo

    @cargo.setter
    def cargo(self, cargo : Cargo):
        self._cargo = cargo

    @property
    def salario_base(self):
        return self._salario_base

    def registrar_servico(self):
        return f"{self.nome} registrou um serviço como {self.cargo}."

    def exibir_dados(self):
        return (
            f"Nome: {self.nome}\n"
            f"CPF: {self.cpf}\n"
            f"Telefone: {self.telefone}\n"
            f"Idade: {self.idade}\n"
            f"Email: {self.email}\n"
            f"Cargo: {self.cargo}\n"
            f"Salário Base: R$ {self.salario_base:.2f}"
        )

    def exibir_dados(self):
        pass 