from entidades.funcionario import Funcionario
from entidades.quarto import Quarto

class ServicoDeQuarto:
    def __init__(self, quarto: Quarto, funcionario: Funcionario, tipo_servico: str, valor: float):
        self.__quarto = quarto
        self.__funcionario = funcionario
        self.__tipo_servico = tipo_servico
        self.__valor = valor
        self.__status = "solicitado"

    @property
    def quarto(self):
        return self.__quarto

    @property
    def funcionario(self):
        return self.__funcionario

    @property
    def tipo_servico(self):
        return self.__tipo_servico

    @property
    def valor(self):
        return self.__valor

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, novo_status: str):
        estados_validos = ["solicitado", "em andamento", "concluído", "interrompido"]
        if novo_status not in estados_validos:
            raise ValueError(f"Status inválido: '{novo_status}'.")
        self.__status = novo_status
