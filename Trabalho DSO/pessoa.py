
from abc import ABC, abstractmethod

class Pessoa(ABC):

    #removi o @abstractmethod, pois implementamos o __init__
    def __init__(self, cpf: str, nome: str, idade: int, telefone: str, email: str):
      if not isinstance(cpf, str):
            raise TypeError("CPF deve ser uma string")
      if not isinstance(nome, str):
            raise TypeError("Nome deve ser uma string")
      if not isinstance(idade, int):
            raise TypeError("Idade deve ser um inteiro")
      
      self.__cpf = cpf
      self.__nome = nome
      self.__idade = idade
      self.__telefone = telefone
      self.__email = email

    @property
    def cpf(self):
      return self.__cpf
  
    @cpf.setter
    def cpf(self,cpf: str):
       if isinstance(cpf, str):
          self.__cpf = cpf
  
    @property
    def nome(self):
       return self.__nome
  
    @nome.setter
    def nome(self,nome: str):
       if isinstance(nome, str):
          self.__nome = nome

    @property
    def idade(self):
        return self.__idade

    @idade.setter
    def idade(self, idade):
        self.__idade = idade

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone):
        self.__telefone = telefone

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email    

    def incluir(self):
       pass

    def excluir(self):
       pass   

    def alterar(self):
       pass

    def listar(self):
       pass     