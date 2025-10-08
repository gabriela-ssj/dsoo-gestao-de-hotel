class TelaFuncionario:
    def tela_opcoes(self):
        print("\n-------- MENU FUNCIONÁRIOS ----------")
        print("1 - Cadastrar Funcionário")
        print("2 - Listar Funcionários")
        print("3 - Excluir Funcionário")
        print("0 - Retornar")
        return int(input("Escolha a opção: "))

    def pega_dados_funcionario(self):
        print("\n--- DADOS DO FUNCIONÁRIO ---")
        nome = input("Nome: ")
        cpf = input("CPF: ")
        idade = int(input("Idade: "))
        telefone = input("Telefone: ")
        email = input("Email: ")
        tipo_cargo = input("Cargo: ")
        return {
            "nome": nome,
            "cpf": cpf,
            "idade": idade,
            "telefone": telefone,
            "email": email,
            "tipo_cargo": tipo_cargo
        }

    def seleciona_funcionario(self):
        return input("Digite o CPF do funcionário: ")

    def mostra_lista(self, lista):
        print("\n--- FUNCIONÁRIOS CADASTRADOS ---")
        for item in lista:
            print(item)

    def mostra_mensagem(self, msg):
        print(msg)
