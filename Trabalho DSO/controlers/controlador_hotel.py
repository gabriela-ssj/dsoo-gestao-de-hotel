from entidades.hotel import Hotel
from telas.tela_hotel import TelaHotel
from collections import Counter

from controlers.controlador_hospede import ControladorHospede
from controlers.controlador_funcionario import ControladorFuncionario
from controlers.controlador_cargo import ControladorCargo
from controlers.controlador_quartos import ControladorQuarto
from controlers.controlador_reserva import ControladorReserva
from controlers.controlador_pagamento import ControladorPagamento
from controlers.controlador_recursos_humanos import ControladorRh
from controlers.controlador_servicodequarto import ControladorServicoDeQuarto

class ControladorHotel:
    def __init__(self, hotel: Hotel):
        self.__hotel = hotel
        self.__tela = TelaHotel()
        self.__controlador_hospede = ControladorHospede()
        self.__controlador_cargo = ControladorCargo()
        self.__controlador_funcionario = ControladorFuncionario(self.__controlador_cargo)
        self.__controlador_quarto = ControladorQuarto()

        self.__controlador_servico_de_quarto = ControladorServicoDeQuarto(
            self.__controlador_quarto,
            self.__controlador_funcionario
        )
        
        self.__controlador_reserva = ControladorReserva(
            self.__controlador_hospede,
            self.__controlador_quarto,
            self.__controlador_funcionario
        )

        self.__controlador_pagamento = ControladorPagamento(self.__controlador_reserva)
        self.__controlador_rh = ControladorRh(self.__controlador_cargo, self.__controlador_funcionario)

    def relatorio_quartos_mais_reservados(self):
        todas_reservas = self.__controlador_reserva.reservas
        total_reservas = len(todas_reservas)
        contador = Counter()
        for reserva in todas_reservas:
            for quarto in reserva.quartos:
                contador[quarto.numero] += 1
        relatorio = []
        if not total_reservas:
            self.__tela.mostra_mensagem("Nenhuma reserva para gerar relatório de quartos.")
            return

        for numero, total in contador.items():
            porcentagem = (total / total_reservas) * 100
            relatorio.append(f"Quarto {numero}: {total} reservas ({porcentagem:.1f}%)")
        self.__tela.mostra_lista(relatorio)

    def retornar(self):
        self.tela_aberta = False

    def abre_tela(self):
        self.tela_aberta = True
        opcoes = {
            1: self.__controlador_hospede.abre_tela,
            2: self.__controlador_quarto.abre_tela,
            3: self.__controlador_reserva.abre_tela,
            4: self.__controlador_pagamento.abre_tela,
            5: self.__controlador_rh.abre_tela,
            6: self.relatorio_quartos_mais_reservados,
            7: self.__controlador_servico_de_quarto.abre_tela, 
            0: self.retornar
        }
        while self.tela_aberta:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
            else:
                self.__tela.mostra_mensagem("Opção inválida.")
