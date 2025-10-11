from entidades.pet import Pet
from typing import List
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
        cpf_hospede, dados_pet = self.__tela.pega_dados_pet()
        hospede = self.__controlador_hospede.buscar_hospede(cpf_hospede)

        if not hospede:
            self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf_hospede} não encontrado.")
            return

        pet = Pet(**dados_pet)
        hospede.adicionar_pet(pet)
        self.__pets.append(pet)
        self.__tela.mostra_mensagem(f"✅ Pet '{pet.nome_pet}' cadastrado para o hóspede '{hospede.nome}'.")

    def listar_pets(self):
        if not self.__pets:
            self.__tela.mostra_mensagem("Nenhum pet cadastrado.")
            return

        lista = [f"{p.nome_pet} | Espécie: {p.especie} | Quantidade: {p.quant_pet}" for p in self.__pets]
        self.__tela.mostra_lista(lista)

    def remover_pet(self):
        cpf_hospede, nome_pet = self.__tela.seleciona_pet()
        hospede = self.__controlador_hospede.buscar_hospede(cpf_hospede)

        if not hospede:
            self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf_hospede} não encontrado.")
            return

        pet_encontrado = next((p for p in hospede.pets if p.nome_pet == nome_pet), None)
        if pet_encontrado:
            hospede.remover_pet(pet_encontrado)
            if pet_encontrado in self.__pets:
                self.__pets.remove(pet_encontrado)
            self.__tela.mostra_mensagem(f"✅ Pet '{nome_pet}' removido do hóspede '{hospede.nome}'.")
        else:
            self.__tela.mostra_mensagem(f"⚠️ Pet '{nome_pet}' não encontrado para este hóspede.")

    def alterar_pet(self):
        cpf_hospede, nome_pet = self.__tela.seleciona_pet()
        hospede = self.__controlador_hospede.buscar_hospede(cpf_hospede)

        if not hospede:
            self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf_hospede} não encontrado.")
            return

        pet_encontrado = next((p for p in hospede.pets if p.nome_pet == nome_pet), None)
        if pet_encontrado:
            _, novos_dados = self.__tela.pega_dados_pet()
            pet_encontrado.nome_pet = novos_dados["nome_pet"]
            pet_encontrado.especie = novos_dados["especie"]
            pet_encontrado.quant_pet = novos_dados["quant_pet"]
            self.__tela.mostra_mensagem(f"✅ Pet '{nome_pet}' alterado com sucesso.")
        else:
            self.__tela.mostra_mensagem(f"⚠️ Pet '{nome_pet}' não encontrado para este hóspede.")

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
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")
