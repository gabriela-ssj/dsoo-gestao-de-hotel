class TelaPagamento:
    def tela_opcoes(self):
        print("\n-------- MENU PAGAMENTO ----------")
        print("1 - Realizar Pagamento")
        print("2 - Alterar Método de Pagamento")
        print("3 - Exibir Comprovante")
        print("0 - Retornar")
        return int(input("Escolha a opção: "))

    def pega_valor_pagamento(self):
        return float(input("Digite o valor a ser pago: "))

    def pega_metodo_pagamento(self):
        return input("Digite o novo método de pagamento: ")

    def mostra_mensagem(self, msg):
        print(msg)
