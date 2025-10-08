from entidades.hospede import Hospede
from entidades.pet import Pet
from typing import List, Optional
from telas.tela_hospede import TelaHospede

class ControladorHospede:
    def __init__(self, controlador_pet=None):
        self.__hospedes: List[Hospede] = []
        self.__controlador_pet = controlador_pet
        self.__tela = TelaHospede()

    def abre_tela(self):
        opcoes = {
            1: self.cadastrar_hospede_via_tela,
            2: self.listar_hospedes_via_tela,
            3: self.excluir_hospede_via_tela,
            4: self.gerenciar_pets_via_tela,
            0: lambda: print("Retornando...")
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
                if opcao == 0:
                    break
            else:
                self.__tela.mostra_mensagem("Opção inválida.")

    # Métodos adaptados para usar a tela
    def cadastrar_hospede_via_tela(self):
        dados = self.__tela.pega_dados_hospede()
        self.cadastrar_hospede(**dados)

    def listar_hospedes_via_tela(self):
        if not self.__hospedes:
            self.__tela.mostra_mensagem("Nenhum hóspede cadastrado.")
        else:
            lista = [f"{h.nome} | CPF: {h.cpf} | Idade: {h.idade}" for h in self.__hospedes]
            self.__tela.mostra_lista(lista)

    def excluir_hospede_via_tela(self):
        cpf = self.__tela.seleciona_hospede()
        self.excluir_hospede(cpf)

    def gerenciar_pets_via_tela(self):
        if self.__controlador_pet:
            cpf = self.__tela.seleciona_hospede()
            hospede = self.buscar_hospede(cpf)
            if hospede:
                self.__controlador_pet.abre_tela(hospede)
            else:
                self.__tela.mostra_mensagem("Hóspede não encontrado.")
