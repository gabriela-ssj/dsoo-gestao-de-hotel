from telas.tela_abstrata import TelaAbstrata

class TelaPet(TelaAbstrata):
    def tela_opcoes(self):
        print("\n-------- MENU PETS ----------")
        print("1 - Cadastrar Pet")
        print("2 - Listar Pets")
        print("3 - Remover Pet")
        print("4 - Alterar Pet")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

    def pega_dados_pet(self):
        print("\n--- DADOS DO PET ---")
        nome_pet = self.le_string("Nome do pet: ")
        especie = self.le_string("Espécie: ")
        dados_pet = {"nome_pet": nome_pet, "especie": especie}
        return dados_pet

    def seleciona_pet(self):
        cpf_hospede = self.valida_cpf("CPF do tutor: ")
        nome_pet = self.le_string("Nome do pet: ")
        return cpf_hospede, nome_pet

    def mostra_lista(self, lista):
        print("\n--- LISTA DE PETS ---")
        for item in lista:
            print(item)
        print()

    def mostra_mensagem(self, msg):
        print(msg)
