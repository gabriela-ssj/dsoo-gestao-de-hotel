class Cargo:
    _salarios_por_cargo_map = {
        "gerente": 5000.0,
        "recepcionista": 2500.0,
        "camareira": 2200.0,
        "cozinheira": 2300.0,
        "limpeza": 2000.0,
        "servicosgerais": 2100.0,
        "arrumadeira": 2500.0,
    }

    def __init__(self, tipo_cargo: str, salario: float):
        if not isinstance(tipo_cargo, str) or not tipo_cargo.strip():
            raise ValueError("Tipo de cargo deve ser uma string não vazia.")
        if not isinstance(salario, (int, float)) or salario < 0:
            raise ValueError("Salário deve ser um número positivo.")

        self._tipo_cargo = tipo_cargo.lower()
        self._salario_base = float(salario)

    @property
    def tipo_cargo(self) -> str:
        """Retorna o nome (string) do tipo de cargo."""
        return self._tipo_cargo

    @tipo_cargo.setter
    def tipo_cargo(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Tipo de cargo deve ser uma string não vazia.")
        valor_lower = valor.lower()
        if valor_lower in Cargo._salarios_por_cargo_map:
            self._salario_base = Cargo._salarios_por_cargo_map[valor_lower]
        self._tipo_cargo = valor_lower

    @property
    def salario_base(self) -> float:
        """Retorna o salário base (float) do cargo."""
        return self._salario_base

    @salario_base.setter
    def salario_base(self, valor: float):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("Salário base deve ser um número positivo.")
        self._salario_base = float(valor)

    def calcular_bonus(self) -> float:
        """Calcula um bônus de 10% sobre o salário base."""
        return self._salario_base * 0.1

    def __str__(self) -> str:
        """Representação em string do objeto Cargo para exibição legível."""
        return f"{self._tipo_cargo.capitalize()} (R\${self._salario_base:.2f})"

    def __eq__(self, other):
        """Define como comparar objetos Cargo (pelo tipo de cargo)."""
        if isinstance(other, Cargo):
            return self.tipo_cargo == other.tipo_cargo
        return False
    
    def __hash__(self):
        """Define o hash para permitir que objetos Cargo sejam usados em conjuntos/dicionários."""
        return hash(self.tipo_cargo)
