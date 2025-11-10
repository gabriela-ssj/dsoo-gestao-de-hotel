from typing import List, Optional

from entidades.hospede import Hospede
from telas.tela_hospede import TelaHospede
from controlers.controlador_pet import ControladorPet

from entidades.pet import Pet


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
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
                if opcao == 0:
                    break
            else:
                self.__tela.mostra_mensagem("Opção inválida.")

    def cadastrar_hospede_via_tela(self):
        dados = self.__tela.pega_dados_hospede()

        if not dados:
            self.__tela.mostra_mensagem("Operação de cadastro de hóspede cancelada.")
            return

        cpf_para_cadastro = dados["cpf"]

        hospede_existente = self.busca_hospede(cpf=cpf_para_cadastro)
        
        if hospede_existente:
            self.__tela.mostra_mensagem(f"Erro: Já existe um hóspede cadastrado com o CPF '{cpf_para_cadastro}'.")
            return 

        nome = dados["nome"]
        telefone = dados["telefone"]

        idade = int(dados["idade"]) 
        email = dados["email"]
        
        hospede = Hospede(
            nome=nome,
            cpf=cpf_para_cadastro, 
            telefone=telefone,
            idade=idade,
            email=email
        )
        self.cadastrar_hospede(hospede)
        self.__tela.mostra_mensagem(f"Hóspede '{hospede.nome}' cadastrado com sucesso!")

    def alterar_hospede_via_tela(self):
        hospede = self.busca_hospede() 
        
        if hospede:
            novos_dados = self.__tela.pega_dados_hospede(hospede_existente=hospede)
            if not novos_dados:
                self.__tela.mostra_mensagem("Operação de alteração cancelada.")
                return

            if novos_dados["cpf"] != hospede.cpf:
                hospede_com_novo_cpf = self.busca_hospede(cpf=novos_dados["cpf"])
                if hospede_com_novo_cpf:
                    self.__tela.mostra_mensagem(f"Erro: O novo CPF '{novos_dados['cpf']}' já pertence a outro hóspede.")
                    return

            hospede.cpf = novos_dados["cpf"]
            hospede.nome = novos_dados["nome"]
            hospede.idade = int(novos_dados["idade"])
            hospede.telefone = novos_dados["telefone"]
            hospede.email = novos_dados["email"]

            self.__tela.mostra_mensagem("Hóspede alterado com sucesso.")
        else:
            self.__tela.mostra_mensagem("Hóspede não encontrado para alteração.")

    def cadastrar_hospede(self, hospede: Hospede):
        self.__hospedes.append(hospede)

    def listar_hospedes_via_tela(self):
        if not self.__hospedes:
            self.__tela.mostra_mensagem("Nenhum hóspede cadastrado.")
        else:
            lista = [f"{h.nome} | CPF: {h.cpf} | Idade: {h.idade}" for h in self.__hospedes]
            self.__tela.mostra_lista(lista)

    def excluir_hospede_via_tela(self):
        hospede_para_excluir = self.busca_hospede()
        
        if hospede_para_excluir:
            confirmar = self.__tela.le_string(f"Deseja realmente excluir o hóspede {hospede_para_excluir.nome} (CPF: {hospede_para_excluir.cpf})? (sim/nao): ")
            if confirmar.lower() == "sim":
                self.excluir_hospede(hospede_para_excluir)
                self.__tela.mostra_mensagem(f"Hóspede {hospede_para_excluir.nome} excluído com sucesso.")
            else:
                self.__tela.mostra_mensagem("Operação de exclusão cancelada.")
        else:
            self.__tela.mostra_mensagem("Hóspede não encontrado para exclusão.")

    def busca_hospede(self, cpf: str = None) -> Optional[Hospede]:
        hospede_encontrado = None
        cpf_para_buscar = cpf

        if not self.__hospedes:
            if cpf is None:
                self.__tela.mostra_mensagem("Nenhum hóspede cadastrado no sistema.")
            return None 
        
        while hospede_encontrado is None:
            if cpf_para_buscar is None:
                cpf_digitado_pelo_usuario = self.__tela.seleciona_hospede()
                if not cpf_digitado_pelo_usuario:
                    self.__tela.mostra_mensagem("Busca de hóspede cancelada.")
                    return None
                cpf_para_buscar = cpf_digitado_pelo_usuario

            for hospede_obj in self.__hospedes:
                if hospede_obj.cpf == cpf_para_buscar:
                    hospede_encontrado = hospede_obj
                    break

            if hospede_encontrado is None:
                self.__tela.mostra_mensagem(f"Hóspede com CPF '{cpf_para_buscar}' não encontrado. Por favor, tente novamente.")
                cpf_para_buscar = None 
                if cpf is not None: 
                    return None

        return hospede_encontrado


    def excluir_hospede(self, hospede: Hospede):
        if hospede:
            self.__hospedes.remove(hospede)
            self.__tela.mostra_mensagem(f"Hóspede {hospede.nome} removido do sistema.")
        else:
            self.__tela.mostra_mensagem("Erro: Objeto hóspede inválido para exclusão.")

    def gerenciar_pets_via_tela(self):
        self.__controlador_pet.abre_tela()
