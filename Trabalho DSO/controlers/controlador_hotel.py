from telas.tela_hotel import TelaHotel
from entidades.hotel import Hotel
from entidades.hospede import Hospede
from entidades.quarto import Quarto
from entidades.reserva import Reserva
from collections import Counter
from typing import List

class ControladorHotel:
    def __init__(self, controlador_sistema, hotel: Hotel):
        self.__hotel = hotel
        self.__tela_hotel = TelaHotel()
        self.__controlador_sistema = controlador_sistema

    def adicionar_hospede(self, hospede: Hospede):
        duplicado = False
        for h in self.__hotel.hospedes:
            if h.cpf == hospede.cpf:
                print(f"ATENÇÃO: Hóspede com CPF {hospede.cpf} já está cadastrado.")
                duplicado = True
        if not duplicado:
            self.__hotel.adicionar_hospede(hospede)

    def excluir_hospede(self, cpf: str):
        self.__hotel.excluir_hospede(cpf)

    def listar_hospedes(self) -> List[str]:
        return self.__hotel.listar_hospedes()

    def adicionar_quarto(self, quarto: Quarto):
        self.__hotel.adicionar_quarto(quarto)

    def excluir_quarto(self, numero: int):
        self.__hotel.excluir_quarto(numero)

    def alterar_quarto(self, numero: int, novos_dados: dict):
        self.__hotel.alterar_quarto(numero, novos_dados)

    def listar_quartos(self) -> List[str]:
        return self.__hotel.listar_quartos()

    def adicionar_reserva(self, nova_reserva: Reserva):
        self.__hotel.adicionar_reserva(nova_reserva)

    def listar_reservas(self) -> List[str]:
        return self.__hotel.listar_reservas()

    def relatorio_quartos_mais_reservados(self):
        total_reservas = len(self.__hotel.reservas)
        contador = Counter()

        for reserva in self.__hotel.reservas:
            for quarto in reserva.quartos:
                contador[quarto.numero] += 1

        print("\n--- RELATÓRIO DE USO DE QUARTOS ---")
        for numero, total in contador.items():
            porcentagem = (total / total_reservas) * 100 if total_reservas else 0
            print(f"Quarto {numero}: {total} reservas ({porcentagem:.1f}%)")
