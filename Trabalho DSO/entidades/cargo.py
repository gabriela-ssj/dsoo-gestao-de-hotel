
from typing import Optional

class Cargo:
    _salarios_por_cargo = {
        "gerente": 5000.0,
        "recepcionista": 2500.0,
        "camareira": 2200.0,
        "cozinheira": 2300.0,
        "limpeza": 2000.0,
        "serviços gerais": 2100.0
    }

    def __init__(self, tipo_cargo: str, salario_base: Optional[float] = None):
        tipo_cargo_lower = tipo_cargo.lower()
        self._tipo_cargo = tipo_cargo_lower
        
        if salario_base is not None:
            if not isinstance(salario_base, (int, float)) or salario_base <= 0:
                raise ValueError("Salário base fornecido deve ser um número positivo.")
            self._salario_base = float(salario_base)
        elif tipo_cargo_lower in self._salarios_por_cargo:
            self._salario_base = self._salarios_por_cargo[tipo_cargo_lower]
        else:
            raise ValueError(f"Tipo de cargo '{tipo_cargo}' inválido. Não há salário padrão definido. \nOpções válidas com salário padrão: {', '.join(self._salarios_por_cargo.keys())}")

    @property
    def tipo_cargo(self):
        return self._tipo_cargo

    @tipo_cargo.setter
    def tipo_cargo(self, valor):
        valor_lower = valor.lower()

        if valor_lower in self._salarios_por_cargo:

            self._tipo_cargo = valor_lower
            self._salario_base = self._salarios_por_cargo[valor_lower]
        else:

            self._tipo_cargo = valor_lower

    @property
    def salario_base(self):
        return self._salario_base

    @salario_base.setter
    def salario_base(self, novo_salario: float):
        if not isinstance(novo_salario, (int, float)) or novo_salario <= 0:
            raise ValueError("Salário base deve ser um número positivo.")
        self._salario_base = float(novo_salario)

    def calcular_bonus(self):
        return self._salario_base * 0.1
