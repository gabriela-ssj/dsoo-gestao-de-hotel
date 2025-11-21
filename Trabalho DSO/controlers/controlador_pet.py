from entidades.pet import Pet
from entidades.hospede import Hospede
from typing import Optional, Dict, Any, List
from telas.tela_pet import TelaPet
from controlers.ValidacaoException import ValidacaoException
from daos.pet_dao import PetDAO


class ControladorPet:
    def __init__(self, controlador_hospede):
        self.__dao = PetDAO()
        self.__tela = TelaPet()
        self.__controlador_hospede = controlador_hospede

    @property
    def pets(self):
        return list(self.__dao.get_all().values())

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

            self.__dao.add(pet)

            self.__tela.mostra_mensagem(
                f"Pet '{pet.nome_pet}' cadastrado para o hóspede '{hospede.nome}'."
            )

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

        dados_pets = [
            {"nome": pet.nome_pet, "especie": pet.especie}
            for pet in hospede.pets
        ]

        self.__tela.mostra_lista(dados_pets, nome_tutor=hospede.nome)


    def remover_pet(self):
        resultado = self.__tela.seleciona_pet()

        if resultado is None:
            self.__tela.mostra_mensagem("Remoção cancelada.")
            return

        cpf_hospede, nome_pet = resultado

        hospede = self.__controlador_hospede.busca_hospede(cpf_hospede)

        if not hospede:
            self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf_hospede} não encontrado.")
            return

        pet = self.__busca_pet_do_hospede(hospede, nome_pet)

        if not pet:
            self.__tela.mostra_mensagem(f"Pet '{nome_pet}' não encontrado.")
            return

        confirmar = self.__tela.confirma_acao(
            f"Deseja realmente excluir o pet '{nome_pet}' do hóspede '{hospede.nome}'?"
        )

        if not confirmar:
            self.__tela.mostra_mensagem("Operação cancelada.")
            return

        hospede.remover_pet(pet)
        self.__dao.remove(pet.nome_pet)

        self.__tela.mostra_mensagem(f"Pet '{nome_pet}' removido com sucesso.")


    def alterar_pet(self):
        resultado = self.__tela.seleciona_pet()

        if resultado is None:
            self.__tela.mostra_mensagem("Alteração cancelada.")
            return

        cpf_hospede, nome_pet = resultado

        hospede = self.__controlador_hospede.busca_hospede(cpf_hospede)

        if not hospede:
            self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf_hospede} não encontrado.")
            return

        pet = self.__busca_pet_do_hospede(hospede, nome_pet)

        if not pet:
            self.__tela.mostra_mensagem(f"Pet '{nome_pet}' não encontrado.")
            return

        dados_atuais = {"nome_pet": pet.nome_pet, "especie": pet.especie}

        novos_dados = self.__tela.pega_dados_pet(dados_atuais=dados_atuais)

        if not novos_dados:
            self.__tela.mostra_mensagem("Alteração cancelada.")
            return

        novo_nome = novos_dados["nome_pet"]

        if (
            novo_nome.lower() != pet.nome_pet.lower()
            and self.__busca_pet_do_hospede(hospede, novo_nome)
        ):
            self.__tela.mostra_mensagem(f"Já existe um pet chamado '{novo_nome}' para este hóspede.")
            return

        pet.nome_pet = novos_dados["nome_pet"]
        pet.especie = novos_dados["especie"]

        self.__dao.update(pet)

        self.__tela.mostra_mensagem("Pet atualizado com sucesso.")


    def abre_tela(self):
        opcoes = {
            1: self.cadastrar_pet,
            2: self.listar_pets,
            3: self.remover_pet,
            4: self.alterar_pet,
            0: self.retornar,
        }

        while True:
            try:
                opcao = self.__tela.tela_opcoes()
                if opcao == 0:
                    break
                func = opcoes.get(opcao)
                if func:
                    func()
                else:
                    self.__tela.mostra_mensagem("Opção inválida.")
            except ValidacaoException as e:
                self.__tela.mostra_mensagem(str(e))
