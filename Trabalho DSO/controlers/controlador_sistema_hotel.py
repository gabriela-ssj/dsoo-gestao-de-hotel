from entidades.sistema_hotel import SistemaHotel
from entidades.hotel import Hotel
from controlers.controlador_hotel import ControladorHotel
from telas.tela_sistemahotel import TelaSistemaHotel

class ControladorSistemaHotel:
    def __init__(self, controlador_principal):
        self.__sistema_hotel = SistemaHotel()
        self.__tela = TelaSistemaHotel()
        self.__controlador_principal = controlador_principal

    def incluir_hotel(self):
        dados = self.__tela.pega_dados_hotel()
        hotel = Hotel(dados["nome"])
        self.__sistema_hotel.incluir_hotel(hotel)

    def excluir_hotel(self):
        nome = self.__tela.seleciona_hotel()
        self.__sistema_hotel.excluir_hotel(nome)

    def alterar_hotel(self):
        nome = self.__tela.seleciona_hotel()
        hotel = self.__sistema_hotel.buscar_hotel(nome)
        if hotel:
            novos_dados = self.__tela.pega_dados_hotel()
            self.__sistema_hotel.alterar_hotel(nome, novos_dados)
        else:
            self.__tela.mostra_mensagem("⚠️ Hotel não encontrado.")

    def listar_hoteis(self):
        lista = self.__sistema_hotel.listar_hoteis()
        if lista:
            self.__tela.mostra_lista(lista)
        else:
            self.__tela.mostra_mensagem("⚠️ Nenhum hotel cadastrado.")

    def acessar_hotel(self):
        nome = self.__tela.seleciona_hotel()
        hotel = self.__sistema_hotel.buscar_hotel(nome)
        if hotel:
            controlador_hotel = ControladorHotel(self.__controlador_principal, hotel)
            controlador_hotel.abre_tela()
        else:
            self.__tela.mostra_mensagem("⚠️ Hotel não encontrado.")

    def retornar(self):
        self.__controlador_principal.abre_tela()

    def abre_tela(self):
        opcoes = {
            1: self.incluir_hotel,
            2: self.alterar_hotel,
            3: self.listar_hoteis,
            4: self.excluir_hotel,
            5: self.acessar_hotel,
            0: self.retornar
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
            else:
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")
