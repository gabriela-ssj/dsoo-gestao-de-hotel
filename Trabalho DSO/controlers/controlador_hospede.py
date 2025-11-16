from typing import List, Optional
from entidades.hospede import Hospede
from telas.tela_hospede import TelaHospede
from controlers.controlador_pet import ControladorPet
from entidades.pet import Pet
from controlers.ValidacaoException import ValidacaoException


class ControladorHospede:
    def __init__(self):
        self.__hospedes: List[Hospede] = []
        self.__tela = TelaHospede()
        self.__controlador_pet = ControladorPet(self)

    def retornar(self):
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
            try:
                opcao = self.__tela.tela_opcoes()
                if opcao in opcoes:
                    opcoes[opcao]()
                    if opcao == 0:
                        break
                else:
                    self.__tela.mostra_mensagem("Opção inválida.")
            except ValidacaoException as e:
                self.__tela.mostra_mensagem(f"⚠️ {str(e)}")


    def cadastrar_hospede_via_tela(self):
        dados = self.__tela.pega_dados_hospede()

        ValidacaoException.se_none(dados, "Operação cancelada pelo usuário.")

        ValidacaoException.validar_campo_vazio(dados["nome"], "Nome")
        ValidacaoException.validar_campo_vazio(dados["cpf"], "CPF")
        ValidacaoException.validar_campo_vazio(dados["telefone"], "Telefone")
        ValidacaoException.validar_campo_vazio(dados["email"], "Email")

        idade = int(dados["idade"])
        ValidacaoException.validar_idade_valida(idade)
        ValidacaoException.validar_email(dados["email"])

        ValidacaoException.validar_cpf_unico(self.__hospedes, dados["cpf"])

        hospede = Hospede(
            nome=dados["nome"],
            cpf=dados["cpf"],
            telefone=dados["telefone"],
            idade=idade,
            email=dados["email"]
        )

        self.__hospedes.append(hospede)
        self.__tela.mostra_mensagem(f"Hóspede '{hospede.nome}' cadastrado com sucesso!")


    def alterar_hospede_via_tela(self):
        hospede = self.busca_hospede()

        ValidacaoException.se_none(hospede, "Hóspede não encontrado para alteração.")

        novos_dados = self.__tela.pega_dados_hospede(hospede_existente=hospede)

        ValidacaoException.se_none(novos_dados, "Operação cancelada.")

        ValidacaoException.validar_campo_vazio(novos_dados["nome"], "Nome")
        ValidacaoException.validar_campo_vazio(novos_dados["cpf"], "CPF")
        ValidacaoException.validar_campo_vazio(novos_dados["telefone"], "Telefone")

        idade = int(novos_dados["idade"])
        ValidacaoException.validar_idade_valida(idade)
        ValidacaoException.validar_email(novos_dados["email"])

        if novos_dados["cpf"] != hospede.cpf:
            ValidacaoException.validar_cpf_unico(self.__hospedes, novos_dados["cpf"])

        hospede.cpf = novos_dados["cpf"]
        hospede.nome = novos_dados["nome"]
        hospede.idade = idade
        hospede.telefone = novos_dados["telefone"]
        hospede.email = novos_dados["email"]

        self.__tela.mostra_mensagem("Hóspede alterado com sucesso.")


    def listar_hospedes_via_tela(self):
        ValidacaoException.se_vazio(self.__hospedes, "Nenhum hóspede cadastrado.")

        lista = [
            f"{h.nome} | CPF: {h.cpf} | Idade: {h.idade}"
            for h in self.__hospedes
        ]
        self.__tela.mostra_lista(lista)


    def excluir_hospede_via_tela(self):
        hospede = self.busca_hospede()

        ValidacaoException.se_none(hospede, "Hóspede não encontrado para exclusão.")

        confirmar = self.__tela.le_string(
            f"Deseja realmente excluir '{hospede.nome}' (CPF {hospede.cpf})? (sim/nao): "
        )

        if confirmar.lower() != "sim":
            raise ValidacaoException("Operação cancelada.")

        self.__hospedes.remove(hospede)
        self.__tela.mostra_mensagem(f"Hóspede {hospede.nome} removido com sucesso.")


    def busca_hospede(self, cpf: str = None) -> Optional[Hospede]:

        if not self.__hospedes:
            return None

        if cpf is None:
            cpf = self.__tela.seleciona_hospede()
            if not cpf:
                return None

        for h in self.__hospedes:
            if h.cpf == cpf:
                return h

        return None

    def gerenciar_pets_via_tela(self):
        self.__controlador_pet.abre_tela()
