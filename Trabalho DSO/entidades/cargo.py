# entidades/cargo.py
class Cargo:
    _salarios_por_cargo = {
        "gerente": 5000.0,
        "recepcionista": 2500.0,
        "camareira": 2200.0,
        "cozinheira": 2300.0,
        "limpeza": 2000.0,
        "serviços gerais": 2100.0
    }

    def __init__(self, tipo_cargo: str):
        # AQUI, o construtor espera APENAS 'tipo_cargo'
        tipo_cargo = tipo_cargo.lower()
        if tipo_cargo not in self._salarios_por_cargo:
            raise ValueError(f"Tipo de cargo inválido: '{tipo_cargo}'. Opções válidas: {', '.join(self._salarios_por_cargo.keys())}")
        self._tipo_cargo = tipo_cargo
        # O salario_base é DEFINIDO INTERNAMENTE com base no tipo_cargo
        self._salario_base = self._salarios_por_cargo[tipo_cargo]

    @property
    def tipo_cargo(self):
        return self._tipo_cargo

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
