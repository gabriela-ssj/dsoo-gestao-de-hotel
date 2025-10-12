class Cargo:

    def __init__(self, tipo_cargo: str, salario: float):
        self._tipo_cargo = tipo_cargo
        self._salario_base = salario

    @property
    def tipo_cargo(self):
        return self._tipo_cargo,self._salario_base

    @tipo_cargo.setter
    def tipo_cargo(self, valor):
        valor = valor.lower()
        if valor not in self._salarios_por_cargo:
            raise ValueError(f"Tipo de cargo inválido: '{valor}'.")
        self._tipo_cargo = valor
        self._salario_base = self._salarios_por_cargo[valor]

    @property
    def salario_base(self):
        return self._salario_base

    def calcular_bonus(self):
        return self._salario_base * 0.1


