from telas.tela_abstrata import TelaAbstrata

class TelaHospede(TelaAbstrata):
    def tela_opcoes(self):
        print("\n-------- MENU HÓSPEDES ----------")
        print("1 - Cadastrar Hóspede")
        print("2 - Listar Hóspedes")
        print("3 - Excluir Hóspede")
        print("4 - Alterar Hóspede")
        print("5 - Gerenciar Pets do Hóspede")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5])

    def pega_dados_hospede(self, hospede_existente=None):
        print("\n--- DADOS DO HÓSPEDE ---")
        cpf = self.valida_cpf()
        nome = input("Nome: ")
        idade = None
        while not idade:
            try:
                idade = int(input("Idade: "))
            except ValueError:
                self.mostra_mensagem("Idade inválida!")
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
