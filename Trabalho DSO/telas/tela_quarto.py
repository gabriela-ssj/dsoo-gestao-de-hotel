from telas.tela_abstrata import TelaAbstrata

class TelaQuarto(TelaAbstrata):
    def tela_opcoes(self):
        print("\n-------- MENU QUARTOS ----------")
        print("1 - Cadastrar Quarto")
        print("2 - Listar Quartos")
        print("3 - Alterar Quarto")
        print("4 - Excluir Quarto")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

    def pega_dados_quarto(self):
        tipo = self.le_string("Tipo do quarto (suite/duplo/simples): ")
        numero = self.le_num_inteiro("Número base do quarto: ")
        valor_diaria = float(input("Valor da diária: "))
        disponibilidade = self.le_string("Disponível? (s/n): ") == "s"
        hidro = False
        if tipo == "suite":
            hidro = self.le_string("Possui hidromassagem? (s/n): ") == "s"
        return {
            "tipo": tipo,
            "numero": numero,
            "valor_diaria": valor_diaria,
            "disponibilidade": disponibilidade,
            "hidro": hidro
        }

    def seleciona_quarto(self):
        return self.le_string("Digite o número completo do quarto (ex: S101, D202, Q303): ")

    def mostra_lista(self, lista):
        print("\n--- LISTA DE QUARTOS ---")
        for item in lista:
            print(item)
        print()

    def mostra_mensagem(self, msg):
        print(msg)
