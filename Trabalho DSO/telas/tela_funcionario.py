from telas.tela_abstrata import TelaAbstrata
import re

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

        while True:
            nome = input("Nome: ").strip()
            if nome == "":
                self.mostra_mensagem("⚠️ Nome não pode estar vazio.")
            elif not all(c.isalpha() or c.isspace() for c in nome):
                self.mostra_mensagem("⚠️ O nome deve conter apenas letras.")
            else:
                break

        try:
            cpf = self.valida_cpf()
        except Exception as e:
            self.mostra_mensagem(f"Erro ao validar CPF: {e}")
            return None

        while True:
            try:
                idade_str = input("Idade: ").strip()
                if not idade_str.isdigit():
                    raise ValueError("A idade deve ser um número inteiro.")

                idade = int(idade_str)
                if idade < 16 or idade > 120:
                    raise ValueError("Idade fora da faixa permitida (16 a 120).")

                break
            except Exception as e:
                self.mostra_mensagem(f"⚠️ Erro: {e}")

        while True:
            telefone = input("Telefone: ").strip()
            if telefone.isdigit() and (8 <= len(telefone) <= 15):
                break
            self.mostra_mensagem("⚠️ Telefone inválido. Use apenas números (8 a 15 dígitos).")

        while True:
            email = input("Email: ").strip()
            padrao_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"

            if re.match(padrao_email, email):
                break
            self.mostra_mensagem("⚠️ Email inválido. Exemplo válido: nome@dominio.com")

        while True:
            tipo_cargo = input("Cargo: ").strip()
            if tipo_cargo != "":
                break
            self.mostra_mensagem("⚠️ Cargo não pode ser vazio.")

        try:
            return {
                "nome": nome,
                "cpf": cpf,
                "idade": idade,
                "telefone": telefone,
                "email": email,
                "tipo_cargo": tipo_cargo
            }
        except Exception as e:
            self.mostra_mensagem(f"Erro inesperado ao montar dados: {e}")
            return None

    def seleciona_funcionario(self):
        return input("Digite o CPF do funcionário: ")

    def mostra_lista(self, lista):
        print("\n--- FUNCIONÁRIOS CADASTRADOS ---")
        if not lista:
            print("Nenhum funcionário.")
        for item in lista:
            print(item)

    def mostra_mensagem(self, msg):
        print(msg)
