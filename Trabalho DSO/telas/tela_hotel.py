
class TelaHotel:
    def tela_opcoes(self):
        print("-------- HOTEL ----------")
        print("Escolha a opção")
        print("1 - Adicionar Hóspede")
        print("2 - Alterar Hóspede")
        print("3 - Listar Hóspedes")
        print("4 - Excluir Hóspede")
        print("5 - Adicionar Quarto")
        print("6 - Alterar Quarto")
        print("7 - Listar Quartos")
        print("8 - Excluir Quarto")
        print("9 - Adicionar Reserva")
        print("10 - Listar Reservas")
        print("11 - Mostrar Relatório de quartos mais reservados")
        print("0 - Retornar")
        return int(input("Escolha a opção: "))

    def pega_dados_hospede(self):
        print("---- DADOS DO HÓSPEDE ----")
        nome = input("Nome: ")
        cpf = input("CPF: ")
        idade = int(input("Idade: "))
        telefone = input("Telefone: ")
        email = input("Email: ")
        return {"nome": nome, "cpf": cpf, "idade": idade, "telefone": telefone, "email": email}

    def seleciona_hospede(self):
        return input("Digite o CPF do hóspede: ")

    def pega_dados_quarto(self):
        print("---- DADOS DO QUARTO ----")
        numero = int(input("Número do quarto: "))
        valor_diaria = float(input("Valor da diária: "))
        disponibilidade = input("Disponível (s/n): ").lower() == "s"
        tipo = input("Tipo (suite/duplo/simples): ").lower()
        return {"numero": numero, "valor_diaria": valor_diaria, "disponibilidade": disponibilidade, "tipo": tipo}

    def seleciona_quarto(self):
        return int(input("Digite o número do quarto: "))

    def pega_dados_reserva(self):
        print("---- DADOS DA RESERVA ----")
        data_checkin = input("Data de check-in (dd/mm/yyyy): ")
        data_checkout = input("Data de check-out (dd/mm/yyyy): ")
        return {"checkin": data_checkin, "checkout": data_checkout}

    def mostra_mensagem(self, msg):
        print(msg)

    def mostra_lista(self, lista):
        for item in lista:
            print(item)
