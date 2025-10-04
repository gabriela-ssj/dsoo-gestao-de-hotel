from entidades.reserva import Reserva
from entidades.servico_de_quarto import ServicoDeQuarto
from entidades.pet import Pet
from telas.tela_reserva import TelaReserva

class ControladorReserva:
    def __init__(self, reserva: Reserva, controlador_sistema):
        self.__reserva = reserva
        self.__tela = TelaReserva()
        self.__controlador_sistema = controlador_sistema

    def fazer_reserva(self):
        self.__reserva.fazer_reserva()

    def cancelar_reserva(self):
        self.__reserva.cancelar_reserva()

    def editar_reserva(self):
        dados = self.__tela.pega_dados_edicao()
        self.__reserva.editar_reserva(
            nova_data_checkin=dados.get("checkin"),
            nova_data_checkout=dados.get("checkout"),
            novo_quarto=dados.get("quartos")
        )

    def adicionar_servico(self):
        dados = self.__tela.pega_dados_servico()
        servico = ServicoDeQuarto(**dados)
        self.__reserva.adicionar_servico_quarto(servico)

    def adicionar_pet(self):
        dados = self.__tela.pega_dados_pet()
        pet = Pet(**dados)
        self.__reserva.adicionar_pet(pet)

    def calcular_valor_total(self):
        self.__reserva.calcular_valor_total()

    def exibir_relatorio_por_hospede(self):
        self.__reserva.exibir_relatorio_por_hospede()

    def exibir_relatorio_por_tipo_servico(self):
        self.__reserva.exibir_relatorio_por_tipo_servico()

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes = {
            1: self.fazer_reserva,
            2: self.cancelar_reserva,
            3: self.editar_reserva,
            4: self.adicionar_servico,
            5: self.adicionar_pet,
            6: self.calcular_valor_total,
            7: self.exibir_relatorio_por_hospede,
            8: self.exibir_relatorio_por_tipo_servico,
            0: self.retornar
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
            else:
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")
