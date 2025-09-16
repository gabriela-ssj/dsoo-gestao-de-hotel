
from pessoa import Pessoa
from pet import Pet
from typing import Optional, List

class Hospede(Pessoa):
    def __init__(self, cpf:str, nome:str, idade:int, telefone:str, email:str, pets:Optional[List[Pet]] = None):
        super().__init__(cpf, nome, idade, telefone, email)
        if pets is None:
            self.__pets = []
        else:
            self.__pets = pets

    @property
    def pets(self):
        return self.__pets
    
    def is_adulto(self) -> bool:
        return self.idade > 18

    def is_crianca(self) -> bool:
        return self.idade <= 18
    
    def adicionar_pet(self, pet):
        self.__pets.append(pet)

    def remover_pet(self, pet):
        if pet in self.__pets:
            self.__pets.remove(pet)

    def exibir_dados(self):
        pass 
