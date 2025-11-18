from entidades.pet import Pet
from entidades.hospede import Hospede
from typing import List, Optional, Tuple, Dict, Any
from telas.tela_pet import TelaPet

class ControladorPet:
    def __init__(self, controlador_hospede):
        self.__pets: List[Pet] = []
        self.__tela = TelaPet()
        self.__controlador_hospede = controlador_hospede

    @property
    def pets(self):
        return self.__pets

    def cadastrar_pet(self):
        dados = self.__tela.pega_dados_pet()
        
        if not dados:
            self.__tela.mostra_mensagem("Cadastro de pet cancelado.")
            return

        try:
            cpf_hospede = dados.pop("cpf_hospede") 
        except KeyError:
            self.__tela.mostra_mensagem("Erro: O CPF do hóspede não foi fornecido pela tela.")
            return

        hospede = self.__controlador_hospede.busca_hospede(cpf_hospede)

        if not hospede:
            self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf_hospede} não encontrado.")
            return

        pet = Pet(**dados)
        hospede.adicionar_pet(pet)
        self.__pets.append(pet)
        self.__tela.mostra_mensagem(f"Pet '{pet.nome_pet}' cadastrado para o hóspede '{hospede.nome}'.")

    def listar_pets(self):
        if not self.__pets:
            self.__tela.mostra_mensagem("Nenhum pet cadastrado.")
            return

        lista = [f"{p.nome_pet} | Espécie: {p.especie} | Hóspede: {hospede.nome}"
                 for hospede in self.__controlador_hospede.hospedes
                 for p in hospede.pets]

        if not lista: 
             lista = [f"{p.nome_pet} | Espécie: {p.especie}" for p in self.__pets]

        self.__tela.mostra_lista(lista)

    def remover_pet(self):
        cpf_hospede, nome_pet = self.__tela.seleciona_pet()
        if not cpf_hospede:
            self.__tela.mostra_mensagem("Remoção cancelada.")
            return
            
        hospede = self.__controlador_hospede.busca_hospede(cpf_hospede)

        if not hospede:
            self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf_hospede} não encontrado.")
            return

        pet_encontrado = next((p for p in hospede.pets if p.nome_pet == nome_pet), None)
        if pet_encontrado:
            hospede.remover_pet(pet_encontrado)
            if pet_encontrado in self.__pets:
                self.__pets.remove(pet_encontrado)
            self.__tela.mostra_mensagem(f"Pet '{nome_pet}' removido do hóspede '{hospede.nome}'.")
        else:
            self.__tela.mostra_mensagem(f"Pet '{nome_pet}' não encontrado para este hóspede.")

    def alterar_pet(self):
        cpf_hospede, nome_pet = self.__tela.seleciona_pet()
        if not cpf_hospede:
            self.__tela.mostra_mensagem("Alteração cancelada.")
            return

        hospede = self.__controlador_hospede.busca_hospede(cpf_hospede)

        if not hospede:
            self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf_hospede} não encontrado.")
            return

        pet_encontrado = next((p for p in hospede.pets if p.nome_pet == nome_pet), None)
        if pet_encontrado:
            novos_dados_dict: Dict[str, Any] = self.__tela.pega_dados_pet(modo="alteracao", dados_atuais={"nome_pet": nome_pet, "especie": pet_encontrado.especie})
            if not novos_dados_dict:
                self.__tela.mostra_mensagem("Alteração cancelada pelo usuário.")
                return

            novos_dados_dict.pop("cpf_hospede", None) 
            
            pet_encontrado.nome_pet = novos_dados_dict["nome_pet"]
            pet_encontrado.especie = novos_dados_dict["especie"]
            self.__tela.mostra_mensagem(f"Pet '{nome_pet}' alterado com sucesso.")
        else:
            self.__tela.mostra_mensagem(f"Pet '{nome_pet}' não encontrado para este hóspede.")

    def abre_tela(self):
        opcoes = {
            1: self.cadastrar_pet,
            2: self.listar_pets,
            3: self.remover_pet,
            4: self.alterar_pet,
            0: self.retornar
        }

        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
                if opcao == 0:
                    break
            else:
                self.__tela.mostra_mensagem("Opção inválida.")

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")