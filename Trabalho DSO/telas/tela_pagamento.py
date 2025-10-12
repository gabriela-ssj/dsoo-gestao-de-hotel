from telas.tela_abstrata import TelaAbstrata

class TelaPagamento(TelaAbstrata):
    def tela_opcoes(self):
        print("\n-------- MENU PAGAMENTO ----------")
        print("1 - Realizar Pagamento para Reserva")
        print("2 - Alterar Método de Pagamento de um Pagamento Existente")
        print("3 - Exibir Comprovante de Pagamento")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3])

    def pega_valor_pagamento(self):
        return self.le_float("Digite o valor a ser pago: ")

    def pega_metodo_pagamento(self):
        return self.le_string("Digite o novo método de pagamento (ex: Credito, Debito, Dinheiro, Pix): ")

    def seleciona_reserva_para_pagamento(self):
        print("\n--- SELECIONAR RESERVA PARA PAGAMENTO ---")
        reserva_id = self.le_num_inteiro("Digite o ID da reserva para pagamento: ")
        return reserva_id

    def mostra_comprovante(self, comprovante_dados: dict):
        print("\n--- COMPROVANTE DE PAGAMENTO ---")
        for key, value in comprovante_dados.items():
            if isinstance(value, list):
                print(f"{key.replace('_', ' ').capitalize()}:")
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"{key.replace('_', ' ').capitalize()}: {value}")
        print("----------------------------------")
