class Cargo:
    _tipos_validos = [
        "gerente",
        "recepcionista",
        "camareira",
        "cozinheira",
        "limpeza",
        "serviços gerais"
    ]

    def __init__(self, tipo_cargo: str, salario_base: float):
        tipo_cargo = tipo_cargo.lower()
        if tipo_cargo not in self._tipos_validos:
            raise ValueError(f"Tipo de cargo inválido: '{tipo_cargo}'. Opções válidas: {', '.join(self._tipos_validos)}")
        self._tipo_cargo = tipo_cargo
        self._salario_base = salario_base

    @property
    def tipo_cargo(self):
        return self._tipo_cargo

    @tipo_cargo.setter
    def tipo_cargo(self, valor):
        valor = valor.lower()
        if valor not in self._tipos_validos:
            raise ValueError(f"Tipo de cargo inválido: '{valor}'.")
        self._tipo_cargo = valor

    @property
    def salario_base(self):
        return self._salario_base

    @salario_base.setter
    def salario_base(self, valor):
        if valor < 0:
            raise ValueError("Salário base não pode ser negativo.")
        self._salario_base = valor

    def calcular_bonus(self):
        return self._salario_base * 0.1
