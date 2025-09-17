from hotel import Hotel
from hospede import Hospede
from funcionario import Funcionario
from quarto import Suite, Duplo, Simples
from reserva import Reserva
from servico_de_quarto import ServicoDeQuarto
from pagamento import Pagamento
from cargo import Cargo
from recursos_humanos import Rh
from sistema_hotel import SistemaHotel  

sistema = SistemaHotel()
hotel_ativo = None
pagamentos = []

def menu():
    global hotel_ativo

    while True:
        print("\n--- MENU SISTEMA DE HOTÉIS ---")
        print("0. Selecionar ou criar hotel")
        print("1. Adicionar hóspede")
        print("2. Listar hóspedes")
        print("3. Alterar hóspede")
        print("4. Excluir hóspede")
        print("5. Adicionar funcionário")
        print("6. Listar funcionários")
        print("7. Alterar funcionário")
        print("8. Excluir funcionário")
        print("9. Adicionar quarto")
        print("10. Listar quartos")
        print("11. Alterar quarto")
        print("12. Excluir quarto")
        print("13. Criar reserva")
        print("14. Listar reservas")
        print("15. Adicionar serviço de quarto")
        print("16. Gerar pagamento")
        print("17. Ver comprovante de pagamento")
        print("18. Relatório por hóspede")
        print("19. Relatório por tipo de serviço")
        print("20. Executar teste automático")
        print("21. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("\n--- HOTÉIS DISPONÍVEIS ---")
            hoteis = sistema.listar_hoteis()
            for h in hoteis:
                print(h)
            nome = input("Digite o nome do hotel para selecionar ou criar: ")
            hotel = sistema.buscar_hotel(nome)
            if hotel:
                hotel_ativo = hotel
                print(f"✅ Hotel '{nome}' selecionado.")
            else:
                hotel_ativo = Hotel(nome, recursos_humanos=Rh())
                sistema.incluir_hotel(hotel_ativo)
                print(f"✅ Hotel '{nome}' criado e selecionado.")

        elif hotel_ativo is None:
            print("⚠️ Nenhum hotel selecionado. Use a opção 0 para selecionar ou criar um hotel.")
            continue

        elif opcao == "1":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            idade = int(input("Idade: "))
            telefone = input("Telefone: ")
            email = input("Email: ")
            hospede = Hospede(cpf, nome, idade, telefone, email)
            hotel_ativo.adicionar_hospede(hospede)
            print("✅ Hóspede adicionado.")

        elif opcao == "2":
            for h in hotel_ativo.listar_hospedes():
                print(h)

        elif opcao == "3":
            cpf = input("CPF do hóspede a alterar: ")
            campo = input("Campo a alterar (nome, idade, telefone, email): ")
            valor = input("Novo valor: ")
            if campo == "idade":
                valor = int(valor)
            hotel_ativo.alterar_hospede(cpf, {campo: valor})
            print("✅ Hóspede alterado.")

        elif opcao == "4":
            cpf = input("CPF do hóspede a excluir: ")
            hotel_ativo.excluir_hospede(cpf)
            print("✅ Hóspede excluído.")

        elif opcao == "5":
            nome = input("Nome: ")
            cpf = input("CPF: ")
            idade = int(input("Idade: "))
            telefone = input("Telefone: ")
            email = input("Email: ")
            tipo_cargo = input("Cargo: ").lower()
            cargo = Cargo(tipo_cargo)
            funcionario = Funcionario(cpf, nome, idade, telefone, email, cargo)
            hotel_ativo.adicionar_funcionario(funcionario)
            hotel_ativo.recursos_humanos.incluir_funcionario(funcionario)
            print("✅ Funcionário adicionado.")

        elif opcao == "6":
            for f in hotel_ativo.recursos_humanos.listar_funcionarios():
                print(f)

        elif opcao == "7":
            cpf = input("CPF do funcionário a alterar: ")
            campo = input("Campo a alterar (nome, idade, telefone, email): ")
            valor = input("Novo valor: ")
            if campo == "idade":
                valor = int(valor)
            hotel_ativo.alterar_funcionario(cpf, {campo: valor})
            print("✅ Funcionário alterado.")

        elif opcao == "8":
            cpf = input("CPF do funcionário a excluir: ")
            hotel_ativo.recursos_humanos.excluir_funcionario(cpf)
            hotel_ativo.excluir_funcionario(cpf)
            print("✅ Funcionário excluído.")

        elif opcao == "9":
            tipo = input("Tipo (suite/duplo/simples): ").lower()
            numero = int(input("Número do quarto: "))
            diaria = float(input("Valor da diária: "))
            if tipo == "suite":
                quarto = Suite(numero, diaria, True)
            elif tipo == "duplo":
                quarto = Duplo(numero, diaria, True)
            elif tipo == "simples":
                quarto = Simples(numero, diaria, True)
            else:
                print("Tipo inválido.")
                continue
            hotel_ativo.adicionar_quarto(quarto)
            print("✅ Quarto adicionado.")

        elif opcao == "10":
            for q in hotel_ativo.listar_quartos():
                print(q)

        elif opcao == "11":
            numero = int(input("Número do quarto a alterar: "))
            campo = input("Campo a alterar (valor_diaria, disponibilidade): ")
            valor = input("Novo valor: ")
            if campo == "valor_diaria":
                valor = float(valor)
            elif campo == "disponibilidade":
                valor = valor.lower() == "true"
            hotel_ativo.alterar_quarto(numero, {campo: valor})
            print("✅ Quarto alterado.")

        elif opcao == "12":
            numero = int(input("Número do quarto a excluir: "))
            hotel_ativo.excluir_quarto(numero)
            print("✅ Quarto excluído.")

        elif opcao == "13":
            data_checkin = input("Data check-in (dd/mm/yyyy): ")
            data_checkout = input("Data check-out (dd/mm/yyyy): ")
            hospedes = hotel_ativo._Hotel__hospedes
            quartos = hotel_ativo._Hotel__quartos
            reserva = Reserva(hospedes, quartos, data_checkin, data_checkout, "pendente")
            reserva.fazer_reserva()
            hotel_ativo.adicionar_reserva(reserva)
            print("✅ Reserva criada.")

        elif opcao == "14":
            for r in hotel_ativo.listar_reservas():
                print(r)

        elif opcao == "15":
            numero = int(input("Número do quarto: "))
            tipo_servico = input("Tipo de serviço: ")
            valor = float(input("Valor do serviço: "))
            funcionario = hotel_ativo._Hotel__funcionarios[0]
            quarto = next((q for q in hotel_ativo._Hotel__quartos if q.numero == numero), None)
            if quarto:
                servico = ServicoDeQuarto(quarto, funcionario, tipo_servico, valor)
                hotel_ativo._Hotel__reservas[-1].adicionar_servico_quarto(servico)
                print("✅ Serviço adicionado à reserva.")
            else:
                print("Quarto não encontrado.")

        elif opcao == "16":
            reserva = hotel_ativo._Hotel__reservas[-1]
            metodo = input("Método de pagamento: ")
            pagamento = Pagamento(reserva, metodo)
            valor = float(input("Valor pago: "))
            pagamento.pagar(valor)
            pagamentos.append(pagamento)
            print("✅ Pagamento registrado.")

        elif opcao == "17":
            if pagamentos:
                print(pagamentos[-1].comprovante_pagamento())
            else:
                print("Nenhum pagamento registrado.")

        elif opcao == "18":
            reserva = hotel_ativo._Hotel__reservas[-1]
            relatorio = reserva.relatorio_por_hospede()
            for nome, servicos in relatorio.items():
                print(f"{nome}:")
                for tipo, valor in servicos:
                    print(f"  - {tipo}: R$ {valor:.2f}")

        elif opcao == "19":
            reserva = hotel_ativo._Hotel__reservas[-1]
            relatorio = reserva.relatorio_por_tipo_servico()
            for tipo, total in relatorio.items():
                print(f"{tipo}: R$ {total:.2f}")

        elif opcao == "20":
            print("\n--- TESTE AUTOMÁTICO ---")
            h = Hospede("00011122233", "Teste", 35, "48999999999", "teste@email.com")
            q = Simples(999, 100.0, True)
            hotel_ativo.adicionar_hospede(h)
            hotel_ativo.adicionar_quarto(q)
            r = Reserva([h], [q], "01/10/2025", "03/10/2025", "pendente")
            r.fazer_reserva()
            hotel_ativo.adicionar_reserva(r)
            p = Pagamento(r, "PIX")
            p.pagar(200.0)
            assert p.status == "confirmado", "Pagamento não foi confirmado corretamente"
            print("✅ Teste automático passou com sucesso.")

        elif opcao == "21":
            print("Encerrando o sistema...")
            break
