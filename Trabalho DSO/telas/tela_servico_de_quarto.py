class Tela_Servico_de_Quarto:
    def tela_opcoes(self):
        print("\n-------- MENU SERVIÇO DE QUARTO ----------")
        print("1 - Adicionar Serviço de Quarto")
        print("2 - Listar Serviços de Quarto")
        print("0 - Retornar")
        try
            return int(input("Escolha a opção: "))
        except ValueError:
            print("⚠️ Valor inválido!")
   