class TelaReserva:
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
        print("0 - Retornar")
        return int(input("Escolha a opção: "))

    def pega_dados_edicao(self):
        checkin = input("Nova data de check-in (dd/mm/yyyy) ou Enter para manter: ")
        checkout = input("Nova data de check-out (dd/mm/yyyy) ou Enter para manter: ")
        return {
            "checkin": checkin if checkin else None,
            "checkout": checkout if checkout else None,
            "quartos": None  # Aqui você pode adaptar para selecionar novos quartos
        }

    def pega_dados_servico(self):
        tipo = input("Tipo de serviço: ")
        valor = float(input("Valor do serviço: "))
        funcionario = None  # Adapte conforme necessário
        quarto = None       # Adapte conforme necessário
        return {"tipo_servico": tipo, "valor": valor, "funcionario": funcionario, "quarto": quarto}

    def pega_dados_pet(self):
        nome = input("Nome do pet: ")
        especie = input("Espécie: ")
        quant_pet = int(input("Quantidade: "))
        return {"nome": nome, "especie": especie, "quant_pet": quant_pet}

    def mostra_mensagem(self, msg):
        print(msg)
