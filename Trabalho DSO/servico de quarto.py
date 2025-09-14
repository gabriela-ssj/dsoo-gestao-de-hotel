from funcionario import Funcionario
from quartos import Quarto

class ServicoDeQuarto:
    def __init__(self, quarto, funcionario, tipo_servico: str, valor: float):
        self.__quarto = quarto
        self.__funcionario = funcionario
        self.__tipo_servico = tipo_servico
        self.__valor = valor
        self.__status = "solicitado"

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, novo_status: str):
        estados_validos = ["solicitado", "em andamento", "concluído", "interrompido"]
        if novo_status not in estados_validos:
            raise ValueError(f"Status inválido: '{novo_status}'.")
        self.__status = novo_status

    def solicitar_servico(self):
        self.status = "em andamento"
        return f"Serviço '{self.tipo_servico}' iniciado no quarto {self.quarto.numero} por {self.funcionario.nome}."

    def concluir_servico(self):
        self.status = "concluído"
        return f"Serviço '{self.tipo_servico}' concluído por {self.funcionario.nome} no quarto {self.quarto.numero}."

    def parada_servico(self):
        self.status = "interrompido"
        return f"Serviço '{self.tipo_servico}' foi interrompido no quarto {self.quarto.numero}."
