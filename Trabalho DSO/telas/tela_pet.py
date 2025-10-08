class TelaPet:
    def tela_opcoes(self):
        print("\n-------- MENU PETS ----------")
        print("1 - Cadastrar Pet")
        print("2 - Listar Pets")
        print("3 - Remover Pet")
        print("0 - Retornar")
        try:
            return int(input("Escolha a opção: "))
        except ValueError:
            self.mostra_mensagem("Valor inválido!")
            return -1

    def pega_dados_pet(self):
        print("\n--- CADASTRO DE PET ---")
        cpf_hospede = input("CPF do hóspede: ")
        nome_pet = input("Nome do pet: ")
        especie = input("Espécie: ")
        try:
            quant_pet = int(input("Quantidade: "))
        except ValueError:
            self.mostra_mensagem("Quantidade inválida!")
            return None, None
        dados_pet = {"nome_pet": nome_pet, "especie": especie, "quant_pet": quant_pet}
        return cpf_hospede, dados_pet

    def seleciona_pet_para_remover(self):
        print("\n--- REMOVER PET ---")
        cpf_hospede = input("CPF do hóspede: ")
        nome_pet = input("Nome do pet a remover: ")
        return cpf_hospede, nome_pet

    def mostra_lista(self, lista):
        print("\n--- LISTA DE PETS ---")
        for item in lista:
            print(item)
        print()

    def mostra_mensagem(self, msg):
        print(msg)
