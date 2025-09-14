from quarto import Quarto

class Simples(Quarto):
    def __init__(self, numero, valor_diaria, disponibilidade, capacidade_pessoas):
        super().__init__(numero, valor_diaria, disponibilidade, capacidade_pessoas)