from telas.tela_abstrata import TelaAbstrata

class TelaServicoDeQuarto(TelaAbstrata):
    def tela_opcoes(self):
        print("\n-------- MENU SERVIÇO DE QUARTO ----------")
        print("1 - Solicitar Serviço")
        print("2 - Listar Serviços")
        print("3 - Alterar Status de Serviço")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3])

    def pega_dados_servico(self):
        numero_quarto = self.le_string("Número do quarto (ex: S101): ")
        nome_funcionario = self.le_string("Nome do funcionário: ")
        tipo_servico = self.le_string("Tipo de serviço: ")
        valor = float(input("Valor do serviço: "))
        return {
            "numero_quarto": numero_quarto,
            "nome_funcionario": nome_funcionario,
            "tipo_servico": tipo_servico,
            "valor": valor
        }

    def seleciona_servico(self):
        return self.le_string("Digite o número do quarto para localizar o serviço: ")

    def seleciona_status(self):
        return self.le_string("Novo status (solicitado/em andamento/concluído/interrompido): ")

    def mostra_lista(self, lista):
        print("\n--- SERVIÇOS DE QUARTO ---")
        for item in lista:
            print(item)
        print()
