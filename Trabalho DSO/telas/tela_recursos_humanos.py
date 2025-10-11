from telas.tela_abstrata import TelaAbstrata

class TelaRh(TelaAbstrata):
    def tela_opcoes(self):
        print("\n-------- MENU RH ----------")
        print("1 - Incluir Funcionário")
        print("2 - Alterar Funcionário")
        print("3 - Excluir Funcionário")
        print("4 - Listar Funcionários")
        print("5 - Realizar Pagamento")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5])

    def pega_dados_funcionario(self):
        print("\n--- DADOS DO FUNCIONÁRIO ---")
        nome = self.le_string("Nome: ")
        cpf = self.le_string("CPF: ")
        idade = self.le_num_inteiro("Idade: ")
        telefone = self.le_string("Telefone: ")
        email = self.le_string("Email: ")
        tipo_cargo = self.le_string("Cargo: ")
        return {
            "nome": nome,
            "cpf": cpf,
            "idade": idade,
            "telefone": telefone,
            "email": email,
            "tipo_cargo": tipo_cargo
        }

    def seleciona_funcionario(self):
        return self.le_string("Digite o CPF do funcionário: ")

    def pega_metodo_pagamento(self):
        return self.le_string("Método de pagamento: ")

    def mostra_lista(self, lista):
        print("\n--- FUNCIONÁRIOS CADASTRADOS ---")
        for item in lista:
            print(item)

    def mostra_mensagem(self, msg):
        print(msg)
