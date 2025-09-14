class ServicoDeQuarto:
    def __init__(self):

class ServicoDeQuarto:
    def __init__(self, quarto: Quarto, funcionario: Funcionario, valor: float):
        self.quarto = quarto
        self.funcionario = funcionario
        self.valor = valor
        self.__status = "solicitado"

    def solicitar_servico(self):
        self.status = "em andamento"

    def concluir_servico(self):
        self.status = "concluído"
        return f"Serviço concluído por {self.funcionario.nome} no quarto {self.quarto.numero}"        