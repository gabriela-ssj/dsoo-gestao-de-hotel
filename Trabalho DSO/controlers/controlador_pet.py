from entidades.pet import Pet
from entidades.hospede import Hospede
from typing import List, Optional, Tuple, Dict, Any
from telas.tela_pet import TelaPet
from controlers.ValidacaoException import ValidacaoException # Import necessário

class ControladorPet:
    def __init__(self, controlador_hospede):
        self.__pets: List[Pet] = []
        self.__tela = TelaPet()
        self.__controlador_hospede = controlador_hospede

    @property
    def pets(self):
        return self.__pets

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")
    
    def __solicita_cpf_tutor(self, operacao: str) -> Optional[str]:
        self.__tela.mostra_mensagem(f"--- {operacao} PET ---")

        resultado = self.__tela.seleciona_pet()
        
        if resultado is None:
            return None
        
        cpf_hospede, _ = resultado
        return cpf_hospede

    def __busca_pet_do_hospede(self, hospede: Hospede, nome_pet: str) -> Optional[Pet]:
        return next((p for p in hospede.pets if p.nome_pet.lower() == nome_pet.lower()), None)

    def cadastrar_pet(self):
        cpf_hospede_nome_pet = self.__tela.seleciona_pet()
        
        if cpf_hospede_nome_pet is None:
             self.__tela.mostra_mensagem("Cadastro de pet cancelado.")
             return
        
        cpf_hospede, nome_pet_tentativa = cpf_hospede_nome_pet

        hospede = self.__controlador_hospede.busca_hospede(cpf_hospede)

        if not hospede:
            self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf_hospede} não encontrado.")
            return

        dados = self.__tela.pega_dados_pet(dados_atuais={"nome_pet": nome_pet_tentativa})
        
        if not dados:
            self.__tela.mostra_mensagem("Cadastro de pet cancelado.")
            return

        nome_pet = dados["nome_pet"]
        especie = dados["especie"]

        if self.__busca_pet_do_hospede(hospede, nome_pet):
            self.__tela.mostra_mensagem(f"Pet '{nome_pet}' já cadastrado para o hóspede '{hospede.nome}'.")
            return

        try:
            pet = Pet(nome_pet=nome_pet, especie=especie)
            hospede.adicionar_pet(pet)
            self.__pets.append(pet)
            self.__tela.mostra_mensagem(f"Pet '{pet.nome_pet}' cadastrado para o hóspede '{hospede.nome}'.")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro ao cadastrar pet: {e}")

    def listar_pets(self):
        cpf_hospede = self.__solicita_cpf_tutor("LISTAR")
        
        if not cpf_hospede:
            self.__tela.mostra_mensagem("Listagem cancelada.")
            return

        hospede = self.__controlador_hospede.busca_hospede(cpf_hospede)

        if not hospede:
            self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf_hospede} não encontrado.")
            return

        dados_pets: List[Dict[str, Any]] = []
        for pet in hospede.pets:
            dados_pets.append({
                "nome": pet.nome_pet,
                "especie": pet.especie
            })

        self.__tela.mostra_lista(dados_pets, nome_tutor=hospede.nome)

    def remover_pet(self):
        resultado_selecao = self.__tela.seleciona_pet()
        
        if resultado_selecao is None:
            self.__tela.mostra_mensagem("Remoção cancelada.")
            return
            
        cpf_hospede, nome_pet = resultado_selecao

        hospede = self.__controlador_hospede.busca_hospede(cpf_hospede)

        if not hospede:
            self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf_hospede} não encontrado.")
            return

        pet_encontrado = self.__busca_pet_do_hospede(hospede, nome_pet)
        
        if pet_encontrado:
            confirmar = self.__tela.confirma_acao(f"Deseja realmente excluir o pet '{nome_pet}' do hóspede '{hospede.nome}'?")
            if not confirmar:
                self.__tela.mostra_mensagem("Operação cancelada.")
                return

            hospede.remover_pet(pet_encontrado)
            if pet_encontrado in self.__pets:
                self.__pets.remove(pet_encontrado)
            self.__tela.mostra_mensagem(f"Pet '{nome_pet}' removido do hóspede '{hospede.nome}'.")
        else:
            self.__tela.mostra_mensagem(f"Pet '{nome_pet}' não encontrado para este hóspede.")

    def alterar_pet(self):
        resultado_selecao = self.__tela.seleciona_pet()
        
        if resultado_selecao is None:
            self.__tela.mostra_mensagem("Alteração cancelada.")
            return
            
        cpf_hospede, nome_pet = resultado_selecao

        hospede = self.__controlador_hospede.busca_hospede(cpf_hospede)

        if not hospede:
            self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf_hospede} não encontrado.")
            return

        pet_encontrado = self.__busca_pet_do_hospede(hospede, nome_pet)
        
        if pet_encontrado:
            dados_atuais = {"nome_pet": pet_encontrado.nome_pet, "especie": pet_encontrado.especie}
            novos_dados_dict: Dict[str, Any] = self.__tela.pega_dados_pet(dados_atuais=dados_atuais)
            
            if not novos_dados_dict:
                self.__tela.mostra_mensagem("Alteração cancelada pelo usuário.")
                return

            novo_nome = novos_dados_dict["nome_pet"]
            if novo_nome.lower() != pet_encontrado.nome_pet.lower() and self.__busca_pet_do_hospede(hospede, novo_nome):
                self.__tela.mostra_mensagem(f"Já existe um pet chamado '{novo_nome}' para este hóspede.")
                return

            pet_encontrado.nome_pet = novos_dados_dict["nome_pet"]
            pet_encontrado.especie = novos_dados_dict["especie"]
            self.__tela.mostra_mensagem(f"Pet alterado para '{pet_encontrado.nome_pet}' com sucesso.")
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
            try:
                opcao = self.__tela.tela_opcoes()
                if opcao == 0:
                    break
                    
                if opcao in opcoes:
                    opcoes[opcao]()
                else:
                    self.__tela.mostra_mensagem("Opção inválida.")
            except ValidacaoException as e:
                self.__tela.mostra_mensagem(f"{e}")
