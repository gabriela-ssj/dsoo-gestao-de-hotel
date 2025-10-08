class TelaHospede:
    def tela_opcoes(self):
        print("\n-------- MENU HÓSPEDES ----------")
        print("1 - Cadastrar Hóspede")
        print("2 - Listar Hóspedes")
        print("3 - Excluir Hóspede")
        print("4 - Gerenciar Pets do Hóspede")
        print("0 - Retornar")
        try:
            return int(input("Escolha a opção: "))
        except ValueError:
            self.mostra_mensagem("⚠️ Valor inválido!")
            return -1

    def pega_dados_hospede(self):
        print("\n--- DADOS DO HÓSPEDE ---")
        cpf = input("CPF: ")
        nome = input("Nome: ")
        try:
            idade = int(input("Idade: "))
        except ValueError:
            self.mostra_mensagem("⚠️ Idade inválida!")
            return None
        telefone = input("Telefone: ")
        email = input("Email: ")
        return {"cpf": cpf, "nome": nome, "idade": idade, "telefone": telefone, "email": email}

    def seleciona_hospede(self):
        cpf = input("Digite o CPF do hóspede: ")
        return cpf if cpf else None

    def mostra_lista(self, lista):
        print("\n--- LISTA DE HÓSPEDES ---")
        for item in lista:
            print(item)
        print()

    def mostra_mensagem(self, msg):
        print(msg)
