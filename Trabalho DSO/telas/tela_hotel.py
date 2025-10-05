class TelaHotel:
    def tela_opcoes(self):
        print("-------- MENU DO HOTEL --------")
        print("1 - Cadastro de Hóspede")
        print("2 - Gerenciar Quartos")
        print("3 - Gerenciar Reservas")
        print("4 - Pagamentos")
        print("5 - Recursos Humanos")
        print("6 - Relatório: Quartos mais reservados")
        print("0 - Retornar ao menu anterior")
        return int(input("Escolha a opção: "))

    def mostra_lista(self, lista):
        print("\n--- LISTA ---")
        for item in lista:
            print(item)

    def mostra_mensagem(self, msg):
        print(msg)
