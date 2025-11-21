from typing import List, Optional, Dict, Any
from entidades.hospede import Hospede
from telas.tela_hospede import TelaHospede
from controlers.controlador_pet import ControladorPet
from entidades.pet import Pet
from controlers.ValidacaoException import ValidacaoException
from daos.hospede_dao import HospedeDAO


class ControladorHospede:
    def __init__(self):
        self.__hospede_DAO = HospedeDAO()
        self.__tela = TelaHospede()
        self.__controlador_pet = ControladorPet(self)

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")

    def busca_hospede(self, cpf: str = None) -> Optional[Hospede]:

        hospedes = list(self.__hospede_DAO.get_all())
        if not hospedes:
            return None

        if cpf is None:
            cpf = self.__tela.seleciona_hospede()
            if not cpf:
                return None

        for h in hospedes:
            if h.cpf == cpf:
                return h

        return None

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
                if opcao == 0:
                    break
                if opcao in opcoes:
                    opcoes[opcao]()
                else:
                    self.__tela.mostra_mensagem("Opção inválida.")

            except ValidacaoException as e:
                self.__tela.mostra_mensagem(str(e))

            except Exception as e:
                self.__tela.mostra_mensagem(f"Erro inesperado: {str(e)}")

    def cadastrar_hospede_via_tela(self):
        dados = self.__tela.pega_dados_hospede(modo="cadastro")

        ValidacaoException.se_none(dados, "Operação cancelada.")

        for h in self.__hospede_DAO.get_all():
            if h.cpf == dados["cpf"]:
                raise ValidacaoException("Já existe hóspede com este CPF.")

        hospede = Hospede(
            nome=dados["nome"],
            cpf=dados["cpf"],
            telefone=dados["telefone"],
            idade=dados["idade"],
            email=dados["email"]
        )

        self.__hospede_DAO.add(hospede)
        self.__tela.mostra_mensagem(f"Hóspede '{hospede.nome}' cadastrado com sucesso!")

    def alterar_hospede_via_tela(self):
        hospede = self.busca_hospede()
        ValidacaoException.se_none(hospede, "Hóspede não encontrado.")

        dados_atuais = {
            "cpf": hospede.cpf,
            "nome": hospede.nome,
            "idade": hospede.idade,
            "telefone": hospede.telefone,
            "email": hospede.email
        }

        novos_dados = self.__tela.pega_dados_hospede(modo="alteracao", dados_atuais=dados_atuais)
        ValidacaoException.se_none(novos_dados, "Operação cancelada.")

        if novos_dados["cpf"] != hospede.cpf:
            for h in self.__hospede_DAO.get_all():
                if h.cpf == novos_dados["cpf"]:
                    raise ValidacaoException("Já existe hóspede com este CPF.")

            self.__hospede_DAO.remove(hospede.cpf)
            hospede.cpf = novos_dados["cpf"]

        hospede.nome = novos_dados["nome"]
        hospede.telefone = novos_dados["telefone"]
        hospede.email = novos_dados["email"]
        hospede.idade = novos_dados["idade"]

        self.__hospede_DAO.update(hospede)
        self.__tela.mostra_mensagem("Hóspede alterado com sucesso!")

    def listar_hospedes_via_tela(self):
        hospedes = list(self.__hospede_DAO.get_all())
        ValidacaoException.se_vazio(hospedes, "Nenhum hóspede cadastrado.")

        dados_para_tela = []
        for h in hospedes:
            dados_para_tela.append({
                "nome": h.nome,
                "cpf": h.cpf,
                "idade": h.idade,
                "telefone": h.telefone,
                "email": h.email
            })

        self.__tela.mostra_lista(dados_para_tela)

    def excluir_hospede_via_tela(self):
        hospede = self.busca_hospede()
        ValidacaoException.se_none(hospede, "Hóspede não encontrado.")

        confirmar = self.__tela.confirma_acao(
            f"Deseja realmente excluir '{hospede.nome}' (CPF {hospede.cpf})?"
        )

        if not confirmar:
            raise ValidacaoException("Operação cancelada.")

        self.__hospede_DAO.remove(hospede.cpf)
        self.__tela.mostra_mensagem("Hóspede removido com sucesso.")


    def gerenciar_pets_via_tela(self):
        self.__controlador_pet.abre_tela()

    def popula_hospedes_teste(self):
        try:
            h1 = Hospede("Ana Silva", "11122233344", "999887766", 35, "ana@teste.com")
            h2 = Hospede("Bruno Costa", "55566677788", "888776655", 22, "bruno@teste.com")
            self.__hospede_DAO.add(h1)
            self.__hospede_DAO.add(h2)
        except Exception:
            pass
