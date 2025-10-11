from typing import List, Optional
from entidades.hospede import Hospede
from telas.tela_hospede import TelaHospede
from controlers.controlador_pet import ControladorPet

class ControladorHospede:
    def __init__(self):
        self.__hospedes: List[Hospede] = []
        self.__tela = TelaHospede()
        self.__controlador_pet = ControladorPet(self)
        self.__controlador_pet.set_retorno_callback(self.abre_tela)
        self.__retorno_callback = None  

    def set_retorno_callback(self, callback):
        self.__retorno_callback = callback

    def retornar(self):
        if self.__retorno_callback:
            self.__retorno_callback()
        else:
            self.__tela.mostra_mensagem("Retornando ao menu anterior...")

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

    def cadastrar_hospede_via_tela(self):
        dados = self.__tela.pega_dados_hospede()
        hospede = Hospede(
            nome=dados["nome"],
            cpf=dados["cpf"],
            telefone=dados["telefone"],
            idade=int(dados["idade"]),
            email=dados["email"]
        )
        self.cadastrar_hospede(hospede)
        self.__tela.mostra_mensagem("✅ Hóspede cadastrado com sucesso.")

    def alterar_hospede_via_tela(self):
        hospede = self.busca_hospede()
        if hospede:
            novos_dados = self.__tela.pega_dados_hospede()
            hospede.cpf = novos_dados["cpf"]
            hospede.nome = novos_dados["nome"]
            hospede.idade = int(novos_dados["idade"])
            hospede.telefone = novos_dados["telefone"]
            hospede.email = novos_dados["email"]
            self.__tela.mostra_mensagem("✅ Hóspede alterado com sucesso.")
        else:
            self.__tela.mostra_mensagem("⚠️ Hóspede não encontrado.")

    def cadastrar_hospede(self, hospede: Hospede):
        self.__hospedes.append(hospede)

    def listar_hospedes_via_tela(self):
        if not self.__hospedes:
            self.__tela.mostra_mensagem("Nenhum hóspede cadastrado.")
        else:
            lista = [f"{h.nome} | CPF: {h.cpf} | Idade: {h.idade}" for h in self.__hospedes]
            self.__tela.mostra_lista(lista)

    def excluir_hospede_via_tela(self):
        cpf = self.__tela.seleciona_hospede()
        hospede = self.busca_hospede(cpf)
        self.excluir_hospede(hospede)

    def busca_hospede(self, cpf: Optional[str] = None) -> Optional[Hospede]:
        if not cpf:
            cpf = self.__tela.seleciona_hospede()
        for hospede in self.__hospedes:
            if hospede.cpf == cpf:
                return hospede
        return None

    def excluir_hospede(self, hospede: Optional[Hospede]):
        if hospede:
            self.__hospedes.remove(hospede)
            self.__tela.mostra_mensagem("✅ Hóspede excluído.")
        else:
            self.__tela.mostra_mensagem("⚠️ Hóspede não encontrado.")

    def gerenciar_pets_via_tela(self):
        self.__controlador_pet.set_retorno_callback(self.abre_tela)
        self.__controlador_pet.abre_tela()
