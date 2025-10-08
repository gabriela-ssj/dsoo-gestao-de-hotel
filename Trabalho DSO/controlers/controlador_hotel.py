from entidades.hotel import Hotel
from telas.tela_hotel import TelaHotel
from collections import Counter

class ControladorHotel:
    def __init__(self, hotel: Hotel, controlador_sistema):
        self.__hotel = hotel
        self.__tela = TelaHotel()
        self.__controlador_sistema = controlador_sistema

        self.__controlador_hospede = controlador_sistema.controlador_hospede
        self.__controlador_quarto = controlador_sistema.controlador_quarto
        self.__controlador_reserva = controlador_sistema.controlador_reserva
        self.__controlador_pagamento = controlador_sistema.controlador_pagamento
        self.__controlador_rh = controlador_sistema.controlador_recursos_humanos

    #RELATÓRIO
    def relatorio_quartos_mais_reservados(self):
        total_reservas = len(self.__hotel._Hotel__reservas)
        contador = Counter()
        for reserva in self.__hotel._Hotel__reservas:
            for quarto in reserva.quartos:
                contador[quarto.numero] += 1
        relatorio = []
        for numero, total in contador.items():
            porcentagem = (total / total_reservas) * 100 if total_reservas else 0
            relatorio.append(f"Quarto {numero}: {total} reservas ({porcentagem:.1f}%)")
        self.__tela.mostra_lista(relatorio)

    #FLUXO DE TELAS
    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes = {
            1: self.__controlador_hospede.abre_tela,
            2: self.__controlador_quarto.abre_tela,
            3: self.__controlador_reserva.abre_tela,
            4: self.__controlador_pagamento.abre_tela,
            5: self.__controlador_rh.abre_tela,
            6: self.relatorio_quartos_mais_reservados,
            0: self.retornar
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
            else:
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")
