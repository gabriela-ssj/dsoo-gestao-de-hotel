from typing import List, Optional, Dict, Any
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
                
                if opcao == 0:
                    break
                    
                if opcao in opcoes:
                    opcoes[opcao]()
                else:
                    self.__tela.mostra_mensagem("Opção inválida.")
            except ValidacaoException as e:
                self.__tela.mostra_mensagem(f"{str(e)}")
            except Exception as e:
                 self.__tela.mostra_mensagem(f"Erro inesperado: {str(e)}")


    def cadastrar_hospede_via_tela(self):
        dados = self.__tela.pega_dados_hospede(modo="cadastro")

        ValidacaoException.se_none(dados, "Operação cancelada pelo usuário.")
        ValidacaoException.validar_cpf_unico(self.__hospedes, dados["cpf"])

        hospede = Hospede(
            nome=dados["nome"],
            cpf=dados["cpf"],
            telefone=dados["telefone"],
            idade=dados["idade"],
            email=dados["email"]
        )

        self.__hospedes.append(hospede)
        self.__tela.mostra_mensagem(f"Hóspede '{hospede.nome}' cadastrado com sucesso!")

    def alterar_hospede_via_tela(self):
        hospede = self.busca_hospede()

        ValidacaoException.se_none(hospede, "Hóspede não encontrado para alteração.")

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
            ValidacaoException.validar_cpf_unico(self.__hospedes, novos_dados["cpf"])

        hospede.cpf = novos_dados["cpf"]
        hospede.nome = novos_dados["nome"]
        hospede.idade = novos_dados["idade"]
        hospede.telefone = novos_dados["telefone"]
        hospede.email = novos_dados["email"]

        self.__tela.mostra_mensagem("Hóspede alterado com sucesso.")

    def listar_hospedes_via_tela(self):

        ValidacaoException.se_vazio(self.__hospedes, "Nenhum hóspede cadastrado.")

        dados_para_tabela: List[Dict[str, Any]] = []
        for h in self.__hospedes:
            dados_para_tabela.append({
                "nome": h.nome, 
                "cpf": h.cpf, 
                "idade": h.idade,
                "telefone": h.telefone,
                "email": h.email
            })
            
        self.__tela.mostra_lista(dados_para_tabela)


    def excluir_hospede_via_tela(self):
        hospede = self.busca_hospede()

        ValidacaoException.se_none(hospede, "Hóspede não encontrado para exclusão.")

        confirmar = self.__tela.confirma_acao(
            f"Deseja realmente excluir '{hospede.nome}' (CPF {hospede.cpf})?"
        )

        if not confirmar:
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

    def popula_hospedes_teste(self):
        try:
            h1 = Hospede(nome="Ana Silva", cpf="11122233344", telefone="999887766", idade=35, email="ana@teste.com")
            h2 = Hospede(nome="Bruno Costa", cpf="55566677788", telefone="888776655", idade=22, email="bruno@teste.com")
            self.__hospedes.append(h1)
            self.__hospedes.append(h2)
        except Exception:
            pass
