class TelaCargo:
    def tela_opcoes(self):
        print("\n-------- MENU CARGOS ----------")
        print("1 - Listar Cargos Disponíveis")
        print("2 - Criar Cargo")
        print("0 - Retornar")
        return int(input("Escolha a opção: "))

    def pega_dados_cargo(self):
        tipo_cargo = input("Digite o nome do cargo: ")
        return tipo_cargo

    def mostra_lista(self, lista):
        print("\n--- CARGOS CADASTRADOS ---")
        for item in lista:
            print(f"- {item}")

    def mostra_mensagem(self, msg):
        print(msg)
