from entidades.sistema_hotel import SistemaHotel
from entidades.hotel import Hotel
from controlers.controlador_hotel import ControladorHotel
from telas.tela_sistemahotel import TelaSistemaHotel

class ControladorSistemaHotel:
    def __init__(self):
        self.__controladorasHoteis: list[ControladorHotel] = []
        self.__sistema_hotel = SistemaHotel()
        self.__tela = TelaSistemaHotel()
        self.__retorno_callback = None  

    def set_retorno_callback(self, callback):
        self.__retorno_callback = callback

    def incluir_hotel(self):
        dados = self.__tela.pega_dados_hotel()
        hotel = Hotel(dados["nome"])
        self.__sistema_hotel.incluir_hotel(hotel)
        self.__tela.mostra_mensagem(f"✅ Hotel '{hotel.nome}' incluído com sucesso.")

    def excluir_hotel(self):
        nome = self.__tela.seleciona_hotel()
        self.__sistema_hotel.excluir_hotel(nome)

    def alterar_hotel(self):
        nome = self.__tela.seleciona_hotel()
        hotel = self.__sistema_hotel.buscar_hotel(nome)
        if hotel:
            novos_dados = self.__tela.pega_dados_hotel()
            self.__sistema_hotel.alterar_hotel(nome, novos_dados)
            self.__tela.mostra_mensagem("✅ Hotel alterado com sucesso.")
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
            controladorHotel = self.buscaControlador(hotel)
            if not controladorHotel:
                controladorHotel = ControladorHotel(hotel)
                controladorHotel.set_retorno_callback(self.abre_tela)
                self.__controladorasHoteis.append(controladorHotel)
            controladorHotel.abre_tela()
        else:
            self.__tela.mostra_mensagem("⚠️ Hotel não encontrado.")

    def buscaControlador(self, hotel: Hotel):
        for controladorhotel in self.__controladorasHoteis:
            if controladorhotel._ControladorHotel__hotel == hotel:
                return controladorhotel
        return None

    def retornar(self):
        if self.__retorno_callback:
            self.__retorno_callback()
        else:
            self.__tela.mostra_mensagem("Retornando ao menu anterior...")

    def abre_tela(self):
        self.tela_aberta = True
        opcoes = {
            1: self.incluir_hotel,
            2: self.alterar_hotel,
            3: self.listar_hoteis,
            4: self.excluir_hotel,
            5: self.acessar_hotel,
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
