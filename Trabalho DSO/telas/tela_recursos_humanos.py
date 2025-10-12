from telas.tela_abstrata import TelaAbstrata

class TelaRh(TelaAbstrata):
    def tela_opcoes(self):
        print("\n-------- MENU RH ----------")
        print("1 - Gerenciar Cargos")
        print("2 - Gerenciar Funcionários")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2])

    def pega_metodo_pagamento(self):
        return self.le_string("Método de pagamento: ")

    def mostra_lista(self, lista):
        print("\n--- FUNCIONÁRIOS CADASTRADOS ---")
        for item in lista:
            print(item)

    def mostra_mensagem(self, msg):
        print(msg)
