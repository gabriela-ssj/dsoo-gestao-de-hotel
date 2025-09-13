from pessoa import Pessoa
from pessoa import cpf
from pessoa import nome
from pessoa import idade
from pessoa import telefone
from pessoa import email

class Hospede(Pessoa):
    def __init__(self, ):
        super().__init__(cpf, nome, idade, telefone, email)