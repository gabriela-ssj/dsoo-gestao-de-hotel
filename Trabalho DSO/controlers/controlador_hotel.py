from entidades.hotel import Hotel
from telas.tela_hotel import TelaHotel
from collections import Counter
from controlers.controlador_hospede import ControladorHospede
from controlers.controlador_pet import ControladorPet
from controlers.controlador_funcionario import ControladorFuncionario
from controlers.controlador_quartos import ControladorQuarto
from controlers.controlador_reserva import ControladorReserva
from controlers.controlador_pagamento import ControladorPagamento
from controlers.controlador_recursos_humanos import ControladorRh
from controlers.controlador_servicodequarto import ControladorServicoDeQuarto

class ControladorHotel:
    def __init__(self, hotel: Hotel):
        self.__hotel = hotel
        self.__tela = TelaHotel()
        self.__retorno_callback = None  

        # Inicialização dos controladores
        self.__controlador_hospede = ControladorHospede()
        self.__controlador_pet = ControladorPet(self.__controlador_hospede)
        self.__controlador_quarto = ControladorQuarto()
        self.__controlador_funcionario = ControladorFuncionario()
        self.__controlador_rh = ControladorRh()
        self.__controlador_reserva = ControladorReserva(
            controlador_hospede=self.__controlador_hospede,
            controlador_quarto=self.__controlador_quarto,
            controlador_pet=self.__controlador_pet,
            controlador_funcionario=self.__controlador_funcionario
        )
        self.__controlador_pagamento = ControladorPagamento()
        self.__controlador_servico_quarto = ControladorServicoDeQuarto(
            controlador_quarto=self.__controlador_quarto,
            controlador_funcionario=self.__controlador_funcionario
        )

        # Configura retorno para todos os controladores
        self.__controlador_hospede.set_retorno_callback(self.abre_tela)
        self.__controlador_pet.set_retorno_callback(self.__controlador_hospede.abre_tela)
        self.__controlador_quarto.set_retorno_callback(self.abre_tela)
        self.__controlador_funcionario.set_retorno_callback(self.abre_tela)
        self.__controlador_rh.set_retorno_callback(self.abre_tela)
        self.__controlador_reserva.set_retorno_callback(self.abre_tela)
        self.__controlador_pagamento.set_retorno_callback(self.abre_tela)
        self.__controlador_servico_quarto.set_retorno_callback(self.abre_tela)

    def set_retorno_callback(self, callback):
        self.__retorno_callback = callback

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

    def retornar(self):
        if self.__retorno_callback:
            self.__retorno_callback()
        else:
            self.__tela.mostra_mensagem("Retornando ao menu anterior...")

    def abre_tela(self):
        self.tela_aberta = True
        opcoes = {
            1: self.__controlador_hospede.abre_tela,
            2: self.__controlador_quarto.abre_tela,
            3: self.__controlador_reserva.abre_tela,
            4: self.__controlador_pagamento.abre_tela,
            5: self.__controlador_rh.abre_tela,
            6: self.__controlador_servico_quarto.abre_tela,
            7: self.relatorio_quartos_mais_reservados,
            0: self.retornar
        }
        while self.tela_aberta:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
                if opcao == 0:
                    break
            else:
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")
