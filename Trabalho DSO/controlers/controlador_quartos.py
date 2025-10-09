from abc import ABC, abstractmethod
from telas.tela_quarto import TelaQuarto

class ControladorQuartos(ABC):
    def __init__(self):
        self.__quartos = []
        self.__tela = TelaQuarto()
    
    @property
    def quartos(self):
        return self.__quartos

    def adicionar_quarto(self):
        pass

    def listar_quartos(self):
        if not self.__quartos:
            self.__tela.mostra_mensagem("Nenhum quarto cadastrado.")
            return
        lista = [
            f"{q.numero} - R${q.valor_diaria:.2f} - {'Disponível' if q.disponibilidade else 'Ocupado'}"
            for q in self.__quartos
        ]
        self.__tela.mostra_lista(lista)
    
    def buscar_quarto(self, numero: int):
        for q in self.__quartos:
            if q.numero == numero:
                return q
        return None
