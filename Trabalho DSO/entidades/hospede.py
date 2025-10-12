from entidades.pessoa import Pessoa
from entidades.pet import Pet
from typing import Optional, List

class Hospede(Pessoa):
    def __init__(self, cpf: str, nome: str, idade: int, telefone: str, email: str, pets: Optional[List[Pet]] = None):
        super().__init__(cpf=cpf, nome=nome, idade=idade, telefone=telefone, email=email)
        self.__pets: List[Pet] = pets if pets is not None else []

    @property
    def pets(self) -> List[Pet]:
        return self.__pets

    def is_adulto(self) -> bool:
        return self.idade >= 18

    def is_crianca(self) -> bool:
        return self.idade < 18

    def adicionar_pet(self, pet: Pet) -> None:
        if pet not in self.__pets:
            self.__pets.append(pet)

    def remover_pet(self, pet: Pet) -> None:
        if pet in self.__pets:
            self.__pets.remove(pet)

    def exibir_dados(self) -> dict:
        return {
            "cpf": self.cpf,
            "nome": self.nome,
            "idade": self.idade,
            "telefone": self.telefone,
            "email": self.email,
            "pets": [pet.nome_pet for pet in self.__pets]
        }
