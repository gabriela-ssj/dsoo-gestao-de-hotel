class TelaSistemaHotel(TelaAbstrata):
    def tela_opcoes(self):
        print("\n-------- SISTEMA DE HOTÉIS ----------")
        print("1 - Incluir Hotel")
        print("2 - Alterar Hotel")
        print("3 - Listar Hotéis")
        print("4 - Excluir Hotel")
        print("5 - Acessar Hotel")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5])

    def pega_dados_hotel(self):
        nome = input("Nome do hotel: ")
        return {"nome": nome}

    def seleciona_hotel(self):
        return input("Digite o nome do hotel: ")

    def mostra_lista(self, lista):
        print("\n--- HOTÉIS CADASTRADOS ---")
        for item in lista:
            print(item)

    def mostra_mensagem(self, msg):
        print(msg)
