class Pessoa:
    def __init__(self, nome:str, cpf:str, telefone:str, idade:int, email:str):
        self.__nome = nome
        self.__cpf = cpf
        self.__telefone = telefone
        self.__idade = idade
        self.__email = email
    
    @property
    def nome