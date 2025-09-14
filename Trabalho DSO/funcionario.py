from pessoa import Pessoa

class Funcionario(Pessoa):
    def __init__(self, nome: str, cpf: str, telefone: str, idade: int, email: str, cargo: str):
        super().__init__(nome, cpf, telefone, idade, email)
        self._tipos_validos = [
            "gerente",
            "recepcionista",
            "camareira",
            "cozinheira",
            "limpeza",
            "serviços gerais"
        ]
        cargo = cargo.lower()
        if cargo not in self._tipos_validos:
            raise ValueError(f"Cargo inválido: '{cargo}'. Opções válidas: {', '.join(self._tipos_validos)}")
        self._cargo = cargo
        self._salario_base = self._definir_salario_base(cargo)

    def _definir_salario_base(self, cargo):
        tabela = {
            "gerente": 5000.0,
            "recepcionista": 2500.0,
            "camareira": 2200.0,
            "cozinheira": 2300.0,
            "limpeza": 2000.0,
            "serviços gerais": 2100.0
        }
        return tabela[cargo]

    @property
    def cargo(self):
        return self._cargo

    @cargo.setter
    def cargo(self, valor):
        valor = valor.lower()
        if valor not in self._tipos_validos:
            raise ValueError(f"Cargo inválido: '{valor}'.")
        self._cargo = valor
        self._salario_base = self._definir_salario_base(valor)

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
