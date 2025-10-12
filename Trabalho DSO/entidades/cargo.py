class Cargo:
    _salarios_por_cargo = {
        "gerente": 5000.00,
        "recepcionista": 2500.00,
        "limpeza": 1800.00,
        "cozinha": 2200.00,
        "manutencao": 2000.00
    }

    def __init__(self, tipo_cargo: str, salario: float = None):
        tipo_cargo = tipo_cargo.lower()
        if tipo_cargo not in self._salarios_por_cargo:
            raise ValueError(f"Tipo de cargo inválido: '{tipo_cargo}'.")
        self._tipo_cargo = tipo_cargo
        self._salario_base = salario if salario is not None else self._salarios_por_cargo[tipo_cargo]

    @property
    def tipo_cargo(self) -> str:
        return self._tipo_cargo

    @tipo_cargo.setter
    def tipo_cargo(self, valor: str):
        valor = valor.lower()
        if valor not in self._salarios_por_cargo:
            raise ValueError(f"Tipo de cargo inválido: '{valor}'.")
        self._tipo_cargo = valor
        self._salario_base = self._salarios_por_cargo[valor]

    @property
    def salario_base(self) -> float:
        return self._salario_base

    def calcular_bonus(self) -> float:
        return self._salario_base * 0.1

    def exibir_dados(self) -> str:
        return f"Cargo: {self.tipo_cargo.capitalize()} | Salário Base: R$ {self.salario_base:.2f}"
