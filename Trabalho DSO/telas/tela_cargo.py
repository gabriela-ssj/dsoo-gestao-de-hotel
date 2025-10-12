from telas.tela_abstrata import TelaAbstrata

class TelaCargo(TelaAbstrata):
    def tela_opcoes(self):
        print("\n-------- MENU CARGOS ----------")
        print("1 - Listar Cargos Disponíveis")
        print("2 - Criar Cargo")
        print("3 - Alterar Cargo")
        print("4 - Excluir Cargo")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

    def pega_dados_cargo(self):
        print("\n--- DADOS DO CARGO ---")
        nome = self.le_string("Digite o nome do cargo: ")
        salario = self.le_float("Digite o salário base: R$ ")
        return {
            "nome": nome,
            "salario": salario
        }

    def seleciona_cargo(self):
        return self.le_string("Digite o nome do cargo que deseja selecionar: ")

    def mostra_mensagem(self, msg: str):
        print(msg)

    def mostra_lista(self, lista: list):
        print("\n--- CARGOS CADASTRADOS ---")
        for item in lista:
            print(f"Cargo: {item[0].capitalize()} | Salário: R$ {item[1]:.2f}")
