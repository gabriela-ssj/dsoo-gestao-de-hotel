class Quarto:
    def __init__(self, numero:int, valor_diaria:float, disponibilidade:bool, capacidade_pessoas:int):
        self.__numero = numero
        self.__valor_diaria = valor_diaria
        self.__disponibilidade = disponibilidade
        self.__capacidade_pessoas = capacidade_pessoas

    @property
    def numero(self):
        return self.__numero
    
    @numero.setter
    def numero(self, numero):
        self.__numero = numero

    @property
    def valor_diaria(self):
        return self.__valor_diaria
    
    @valor_diaria.setter
    def valor_diaria(self, valor_diaria):
        self.__valor_diaria = valor_diaria

    @property
    def disponibilidade(self):
        return self.__disponibilidade
    
    @disponibilidade.setter
    def disponibilidade(self, disponibilidade):
        self.__disponibilidade = disponibilidade

    @property
    def capacidade_pessoas(self):
        return self.__capacidade_pessoas
    
    @capacidade_pessoas.setter
    def capacidade_pessoas(self, capacidade_pessoas):
        self.__capacidade_pessoas = capacidade_pessoas

    def reservar_quarto(self):
        if self.__disponibilidade:
            self.__disponibilidade = False
            print(f"Quarto {self.__numero} reservado com sucesso.")
        else:
            print(f"Quarto {self.__numero} já está ocupado.")

    def liberar_quarto(self):
        self.__disponibilidade = True
        print(f"Quarto {self.__numero} liberado.")
        