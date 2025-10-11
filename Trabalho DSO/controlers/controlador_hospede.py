from typing import List, Optional

from entidades.hospede import Hospede
from telas.tela_hospede import TelaHospede
from controlers.controlador_pet import ControladorPet


class ControladorHospede:
    def __init__(self):
        self.__hospedes: List[Hospede] = []
        self.__tela = TelaHospede()
        self.__controlador_pet = ControladorPet(self)

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando...")    

    def retornar(self):
        ControladorHotel().abre_tela()  

    def abre_tela(self):
        opcoes = {
            1: self.cadastrar_hospede_via_tela,
            2: self.listar_hospedes_via_tela,
            3: self.excluir_hospede_via_tela,
            4: self.alterar_hospede_via_tela,
            5: self.gerenciar_pets_via_tela,
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

    # Métodos adaptados para usar a tela
    def cadastrar_hospede_via_tela(self):
        dados = self.__tela.pega_dados_hospede()
        nome = dados["nome"]
        cpf = dados["cpf"]
        telefone = dados["telefone"]
        idade = int(dados["idade"])
        email = dados["email"]
        hospede = Hospede(
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            idade=idade,
            email=email
        )
        self.cadastrar_hospede(hospede)

    def alterar_hospede_via_tela(self):
        hospede = self.busca_hospede()
        if hospede:
            novos_dados = self.__tela.pega_dados_hospede()

            hospede.cpf = novos_dados["cpf"]
            hospede.nome = novos_dados["nome"]
            hospede.idade = novos_dados["idade"]
            hospede.telefone = novos_dados["telefone"]
            hospede.email = novos_dados["email"]

            self.__tela.mostra_mensagem("✅ hospede alterado com sucesso.")
        else:
            self.__tela.mostra_mensagem("⚠️ hospede não encontrado.")

    def cadastrar_hospede(self,hospede):
        self.__hospedes.append(hospede)

    def listar_hospedes_via_tela(self):
        if not self.__hospedes:
            self.__tela.mostra_mensagem("Nenhum hóspede cadastrado.")
        else:
            lista = [f"{h.nome} | CPF: {h.cpf} | Idade: {h.idade}" for h in self.__hospedes]
            self.__tela.mostra_lista(lista)

    def excluir_hospede_via_tela(self):
        cpf = self.__tela.seleciona_hospede()
        self.excluir_hospede(self.busca_hospede(cpf))

    def busca_hospede(self,cpf = None):
        if not cpf:
            cpf = self.__tela.seleciona_hospede()
        for hospede in self.__hospedes:
            if (hospede.cpf == cpf):
                return hospede

    def excluir_hospede(self,hospede):
        if hospede:
            self.__hospedes.remove(hospede)

    def gerenciar_pets_via_tela(self):
        self.__controlador_pet.abre_tela()