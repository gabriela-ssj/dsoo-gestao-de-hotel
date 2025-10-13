from telas.tela_abstrata import TelaAbstrata


class TelaReserva(TelaAbstrata):
    def tela_opcoes(self):
        print("\n-------- MENU RESERVA ----------")
        print("1 - Fazer Reserva")
        print("2 - Listar Reservas")
        print("3 - Cancelar Reserva")
        print("4 - Editar Reserva")
        print("5 - Adicionar Serviço de Quarto a uma Reserva")
        print("6 - Adicionar Pet a uma Reserva")
        print("7 - Calcular Valor Total de uma Reserva")
        print("8 - Relatório por Hóspede")
        print("9 - Relatório por Tipo de Serviço")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def pega_dados_reserva(self):
        print("\n--- DADOS DA NOVA RESERVA ---")
        data_checkin = self.le_string("Data de Check-in (dd/mm/yyyy): ")
        data_checkout = self.le_string("Data de Check-out (dd/mm/yyyy): ")

        cpfs_hospedes_str = self.le_string("CPFs dos hóspedes (separados por vírgula): ")
        numeros_quartos_str = self.le_string("Números dos quartos (separados por vírgula, ex: 101,102,..): ")

        return {
            "data_checkin": data_checkin,
            "data_checkout": data_checkout,
            "cpfs_hospedes": [cpf.strip() for cpf in cpfs_hospedes_str.split(',') if cpf.strip()],
            "numeros_quartos": [num.strip() for num in numeros_quartos_str.split(',') if num.strip()]
        }

    def seleciona_reserva(self):
        # Pode ser pelo ID da reserva ou pelo CPF do hóspede principal e data de check-in
        print("\n--- SELECIONAR RESERVA ---")
        reserva_id = self.le_string("Digite o ID da reserva ou parte do nome do hóspede principal: ")
        return reserva_id

    def pega_dados_edicao(self):
        print("\n--- EDITAR RESERVA ---")
        nova_data_checkin = self.le_string("Nova data de Check-in (dd/mm/yyyy) ou 'manter' para não alterar: ")
        nova_data_checkout = self.le_string("Nova data de Check-out (dd/mm/yyyy) ou 'manter' para não alterar: ")
        novos_numeros_quartos_str = self.le_string(
            "Novos números dos quartos (separados por vírgula, 'manter' para não alterar, 'limpar' para remover todos): ")

        return {
            "nova_data_checkin": nova_data_checkin if nova_data_checkin.lower() != 'manter' else None,
            "nova_data_checkout": nova_data_checkout if nova_data_checkout.lower() != 'manter' else None,
            "novos_numeros_quartos": [num.strip() for num in novos_numeros_quartos_str.split(',') if
                                      num.strip()] if novos_numeros_quartos_str.lower() != 'manter' else [],
            "limpar_quartos": True if novos_numeros_quartos_str.lower() == 'limpar' else False
        }

    def pega_dados_servico(self):
        print("\n--- DADOS DO SERVIÇO DE QUARTO ---")
        tipo_servico = self.le_string("Tipo de serviço: ")
        valor = self.le_float("Valor do serviço: ")
        numero_quarto = self.le_string("Número do quarto (da reserva) para o serviço: ")
        cpf_funcionario = self.valida_cpf("CPF do funcionário responsável pelo serviço: ")
        return {
            "tipo_servico": tipo_servico,
            "valor": valor,
            "numero_quarto": numero_quarto,
            "cpf_funcionario": cpf_funcionario
        }

    def pega_dados_pet(self):
        print("\n--- DADOS DO PET PARA RESERVA ---")
        nome_pet = self.le_string("Nome do pet: ")
        especie = self.le_string("Espécie do pet: ")
        return {"nome_pet": nome_pet, "especie": especie}

    def mostra_detalhes_reserva(self, reserva_dados: dict):
        print("\n--- DETALHES DA RESERVA ---")
        for key, value in reserva_dados.items():
            print(f"{key.replace('_', ' ').capitalize()}: {value}")
        print("---------------------------")

    def mostra_lista_reservas(self, lista_reservas: list):
        print("\n--- LISTA DE RESERVAS ---")
        if not lista_reservas:
            print("Nenhuma reserva cadastrada.")
            return
        for reserva_str in lista_reservas:
            print(reserva_str)
        print()
