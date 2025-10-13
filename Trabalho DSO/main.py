from controlers.controlador_sistema import ControladorSistema


# ------------------- TESTE AUTOMÁTICO ------------------- #
def teste_automatico():
    print("\n🚀 Iniciando teste automático do Sistema de Hotel...\n")

    from entidades.hotel import Hotel
    from controlers.controlador_hotel import ControladorHotel
    from entidades.hospede import Hospede
    from entidades.quartos import Simples, Duplo, Suite
    from entidades.reserva import Reserva
    from datetime import datetime, timedelta

    # Criar hotel e controlador
    hotel = Hotel("Hotel Teste")
    controlador_hotel = ControladorHotel(hotel)

    # Acessar subcontroladores
    ctrl_hospede = controlador_hotel._ControladorHotel__controlador_hospede
    ctrl_quarto = controlador_hotel._ControladorHotel__controlador_quarto
    ctrl_func = controlador_hotel._ControladorHotel__controlador_funcionario
    ctrl_cargo = controlador_hotel._ControladorHotel__controlador_cargo
    ctrl_reserva = controlador_hotel._ControladorHotel__controlador_reserva

    # Criar cargos e funcionário
    print("📋 Cadastrando cargos e funcionário...")
    ctrl_cargo.criar_cargo("gerente", 5000)
    cargo_gerente = ctrl_cargo.buscar_cargo("gerente")
    from entidades.funcionario import Funcionario
    func = Funcionario("Carlos", "111", "99999", 35, "carlos@hotel.com", cargo_gerente)
    ctrl_func.funcionarios.append(func)

    # Cadastrar hóspedes
    print("🏨 Cadastrando hóspedes...")
    h1 = Hospede("Gabriela", "123", "99999", 28, "gabi@email.com")
    h2 = Hospede("Marcos", "124", "88888", 32, "marcos@email.com")
    ctrl_hospede.cadastrar_hospede(h1)
    ctrl_hospede.cadastrar_hospede(h2)

    # Cadastrar quartos
    print("🛏️  Cadastrando quartos...")
    q1 = Simples(101, 100.0, True)
    q2 = Duplo(102, 180.0, True)
    q3 = Suite(201, 300.0, True, True)
    ctrl_quarto._ControladorQuarto__quartos.extend([q1, q2, q3])

    # Criar reservas automáticas
    print("📅 Criando reservas de teste...")
    r1 = Reserva([h1], [q1], datetime.now(), datetime.now() + timedelta(days=2))
    r2 = Reserva([h2], [q1, q2], datetime.now(), datetime.now() + timedelta(days=1))
    ctrl_reserva._ControladorReserva__reservas.extend([r1, r2])

    # Gerar relatório de quartos mais reservados
    print("\n📊 Gerando relatório de quartos mais reservados...\n")
    controlador_hotel._ControladorHotel__tela = type(
        "TelaFake",
        (),
        {"mostra_lista": lambda self, lista: print("\n".join(lista)),
         "mostra_mensagem": print}
    )()
    controlador_hotel.relatorio_quartos_mais_reservados()

    print("\n✅ Teste automático finalizado com sucesso!\n")

# ------------------------------------------------------------------ #


if __name__ == "__main__":
    # Inicializa o sistema normalmente
    sistema = ControladorSistema()

    while True:
        print("\n===== MENU INICIAL =====")
        print("[1] Acessar sistema normalmente")
        print("[2] Rodar teste automático")
        print("[0] Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            sistema.inicializa_sistema()
        elif opcao == "2":
            teste_automatico()
        elif opcao == "0":
            print("Encerrando o programa...")
            break
        else:
            print("⚠️ Opção inválida, tente novamente.")
