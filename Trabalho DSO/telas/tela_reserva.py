from telas.tela_abstrata import TelaAbstrata

class TelaReserva(TelaAbstrata):
    def tela_opcoes(self):
        print("\n-------- MENU RESERVA ----------")
        print("1 - Fazer Reserva")
        print("2 - Cancelar Reserva")
        print("3 - Editar Reserva")
        print("4 - Adicionar Serviço de Quarto")
        print("5 - Adicionar Pet")
        print("6 - Calcular Valor Total")
        print("7 - Relatório por Hóspede")
        print("8 - Relatório por Tipo de Serviço")
        print("9 - Listar Reservas")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def pega_dados_edicao(self):
        checkin = input("Nova data de check-in (dd/mm/yyyy) ou Enter para manter: ")
        checkout = input("Nova data de check-out (dd/mm/yyyy) ou Enter para manter: ")
        return {
            "checkin": checkin if checkin else None,
            "checkout": checkout if checkout else None,
            "quartos": None
        }

    def pega_dados_servico(self):
        tipo = self.le_string("Tipo de serviço: ")
        valor = float(input("Valor do serviço: "))
        funcionario = None
        quarto = None
        return {"tipo_servico": tipo, "valor": valor, "funcionario": funcionario, "quarto": quarto}

    def pega_dados_pet(self):
        nome = self.le_string("Nome do pet: ")
        especie = self.le_string("Espécie: ")
        quant_pet = self.le_num_inteiro("Quantidade: ")
        return {"nome": nome, "especie": especie, "quant_pet": quant_pet}
