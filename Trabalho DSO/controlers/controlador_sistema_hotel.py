from entidades.sistema_hotel import SistemaHotel
from entidades.hotel import Hotel
from controlers.controlador_hotel import ControladorHotel
from telas.tela_sistemahotel import TelaSistemaHotel

from typing import Dict
class ControladorSistemaHotel:
    def __init__(self):
        self.__controladorasHoteis: Dict[str, ControladorHotel] = {}
        self.__sistema_hotel = SistemaHotel()
        self.__tela = TelaSistemaHotel()
        self.tela_aberta = False

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
        nome_hotel = self.__tela.seleciona_hotel()
        hotel_entidade = self.__sistema_hotel.buscar_hotel(nome_hotel)

        if hotel_entidade:
            if nome_hotel in self.__controladorasHoteis:
                controlador_hotel_existente = self.__controladorasHoteis[nome_hotel]
                if controlador_hotel_existente._ControladorHotel__hotel is hotel_entidade:
                    print(f"DEBUG: Reutilizando controlador para '{nome_hotel}' (ID: {id(controlador_hotel_existente)})")
                    controlador_hotel_existente.abre_tela()
                else:
                    print(f"DEBUG: Entidade Hotel para '{nome_hotel}' mudou, recriando controlador.")
                    novo_controlador_hotel = ControladorHotel(hotel_entidade)
                    self.__controladorasHoteis[nome_hotel] = novo_controlador_hotel
                    novo_controlador_hotel.abre_tela()
            else:
                novo_controlador_hotel = ControladorHotel(hotel_entidade)
                self.__controladorasHoteis[nome_hotel] = novo_controlador_hotel
                print(f"DEBUG: Criando novo controlador para '{nome_hotel}' (ID: {id(novo_controlador_hotel)})")
                novo_controlador_hotel.abre_tela()
        else:
            self.__tela.mostra_mensagem("⚠️ Hotel não encontrado.")


    def retornar(self):
        self.tela_aberta = False

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
            else:
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")