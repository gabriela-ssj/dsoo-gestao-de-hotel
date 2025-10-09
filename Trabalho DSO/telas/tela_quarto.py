class TelaQuarto:
    def tela_opcoes(self):
        print("\n------ MENU QUARTOS ------")
        print("1 - Adicionar Quarto")
        print("2 - Listar Quartos")
        print("3 - Remover Quarto")
        print("0 - Retornar")
        try:
            return int(input("Escolha a opção: "))
        except ValueError:
            print("⚠️ Valor inválido!")
            return -1

    def mostra_lista(self, lista):
        print("\n--- LISTA DE QUARTOS ---")
        for item in lista:
            print(item)

    def mostra_mensagem(self, msg):
        print(msg)
