
class TelaHotel():

    def tela_opcoes(self):
    print("-------- HOTEL ----------")
    print("Escolha a opcao")
    print("1 - Adicionar Hospede")
    print("2 - Alterar Hospede")
    print("3 - Listar Hospedes")
    print("4 - Excluir Hospede")
    print("5 - Adicionar Quarto")
    print("6 - Alterar Quarto")
    print("7 - Listar Quartos")
    print("8 - Excluir Quarto")
    print("9 - Adicinar Reserva")
    print("10 - Listar reserva")
    print("11 - Mostrar Relatório de quartos mais reservados")
    print("0 - Retornar")

    opcao = int(input("Escolha a opcao: "))
    return opcao