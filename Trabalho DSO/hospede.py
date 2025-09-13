from pessoa import Pessoa

class Hospede(Pessoa):
    def __init__(self, cpf:str, nome:str, idade:int, telefone:str, email:str):
        super().__init__(cpf, nome, idade, telefone, email)