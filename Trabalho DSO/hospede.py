
from pessoa import Pessoa

class Hospede(Pessoa):
    def __init__(self, cpf:str, nome:str, idade:int, telefone:str, email:str, hosp_adulto:str, hosp_crianca:str ):
        super().__init__(cpf, nome, idade, telefone, email)
        self.__hosp_adulto = hosp_adulto
        self.__hosp_crianca = hosp_crianca
    
    @property
    def hosp_adulto(self):
        return self.__hosp_adulto
    
    @hosp_adulto.setter
    def hosp_adulto(self, hosp_adulto):
        self.__hosp_adulto = hosp_adulto

    @property
    def hosp_crianca(self):
        return self.__hosp_crianca
    
    @hosp_crianca.setter
    def hosp_crianca(self, hosp_crianca):
        self.__hosp_crianca = hosp_crianca

    def verifica_hospede(self):
        pass