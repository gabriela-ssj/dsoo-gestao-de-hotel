class TelaRh:
    def tela_opcoes(self):
        print("\n-------- MENU RH ----------")
        print("1 - Menu Cargos")
        print("2 - Menu Funcionarios")
        print("0 - Retornar")
        return int(input("Escolha a opção: "))

    def pega_metodo_pagamento(self):
        return input("Método de pagamento: ")

    def mostra_lista(self, lista):
        print("\n--- FUNCIONÁRIOS CADASTRADOS ---")
        for item in lista:
            print(item)

    def mostra_mensagem(self, msg):
        print(msg)
