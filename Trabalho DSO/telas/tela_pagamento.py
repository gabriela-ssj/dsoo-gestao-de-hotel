from telas.tela_abstrata import TelaAbstrata

class TelaPagamento(TelaAbstrata):
    def tela_opcoes(self):
        print("\n-------- MENU PAGAMENTO ----------")
        print("1 - Realizar Pagamento")
        print("2 - Alterar Método de Pagamento")
        print("3 - Exibir Comprovante")
        print("4 - Cancelar Pagamento")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

    def pega_valor_pagamento(self):
        return float(input("Digite o valor a ser pago: "))

    def pega_metodo_pagamento(self):
        return self.le_string("Digite o novo método de pagamento: ")

    def mostra_mensagem(self, msg):
        print(msg)
