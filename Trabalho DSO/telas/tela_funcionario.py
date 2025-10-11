from telas.tela_abstrata import TelaAbstrata

class TelaFuncionario(TelaAbstrata):
    def tela_opcoes(self):
        print("\n-------- MENU FUNCIONÁRIOS ----------")
        print("1 - Cadastrar Funcionário")
        print("2 - Listar Funcionários")
        print("3 - Excluir Funcionário")
        print("4 - Alterar Funcionário")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

    def pega_dados_funcionario(self):
        print("\n--- DADOS DO FUNCIONÁRIO ---")
        nome = input("Nome: ")
        cpf = self.valida_cpf()
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
