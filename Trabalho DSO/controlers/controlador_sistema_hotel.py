from entidades.sistema_hotel import SistemaHotel
from entidades.hotel import Hotel
from controlers.controlador_hotel import ControladorHotel
from telas.tela_sistemahotel import TelaSistemaHotel
from typing import Dict, Optional

class ControladorSistemaHotel:
    def __init__(self):
        self.__controladorasHoteis: Dict[str, ControladorHotel] = {}
        self.__sistema_hotel = SistemaHotel()
        self.__tela = TelaSistemaHotel()
        self.tela_aberta = False

    def incluir_hotel(self):
        dados = self.__tela.pega_dados_hotel()
        if not dados or not dados.get("nome"):
            self.__tela.mostra_mensagem("Inclusão cancelada ou dados inválidos.")
            return

        nome_normalizado = dados["nome"].strip().lower()
        hotel = Hotel(nome_normalizado)
        if self.__sistema_hotel.incluir_hotel(hotel):
            self.__tela.mostra_mensagem("Hotel incluído com sucesso.")
        else:
            self.__tela.mostra_mensagem("Já existe um hotel com esse nome.")

    def excluir_hotel(self):
        input_hotel = self.__tela.seleciona_hotel()
        if not input_hotel:
            self.__tela.mostra_mensagem("Operação cancelada.")
            return

        nome = input_hotel.strip().lower()
        
        if self.__sistema_hotel.excluir_hotel(nome):
            self.__tela.mostra_mensagem("Hotel excluído com sucesso.")
        else:
            self.__tela.mostra_mensagem("Hotel não encontrado.")

    def alterar_hotel(self):
        input_hotel = self.__tela.seleciona_hotel()
        if not input_hotel:
            self.__tela.mostra_mensagem("Operação cancelada.")
            return

        nome = input_hotel.strip().lower()
        hotel = self.__sistema_hotel.buscar_hotel(nome)
        
        if hotel:
            novos_dados = self.__tela.pega_dados_hotel()

            if not novos_dados or not novos_dados.get("nome"):
                 self.__tela.mostra_mensagem("Alteração cancelada ou nome inválido.")
                 return
                 
            novos_dados["nome"] = novos_dados["nome"].strip().lower()
            self.__sistema_hotel.alterar_hotel(nome, novos_dados)
            self.__tela.mostra_mensagem("Hotel alterado com sucesso.")
        else:
            self.__tela.mostra_mensagem("Hotel não encontrado.")

    def listar_hoteis(self):
        lista = self.__sistema_hotel.listar_hoteis()
        if lista:
            self.__tela.mostra_lista(lista)
        else:
            self.__tela.mostra_mensagem("Nenhum hotel cadastrado.")

    def acessar_hotel(self):
        input_hotel = self.__tela.seleciona_hotel()
        if not input_hotel:
            self.__tela.mostra_mensagem("Operação cancelada.")
            return

        nome_hotel = input_hotel.strip().lower()

        hotel_entidade = self.__sistema_hotel.buscar_hotel(nome_hotel)

        if hotel_entidade:
            if nome_hotel in self.__controladorasHoteis:
                controlador_hotel_existente = self.__controladorasHoteis[nome_hotel]
                
                if getattr(controlador_hotel_existente, '_ControladorHotel__hotel', None) is hotel_entidade:
                    controlador_hotel_existente.abre_tela()
                else:
                    novo_controlador_hotel = ControladorHotel(hotel_entidade)
                    self.__controladorasHoteis[nome_hotel] = novo_controlador_hotel
                    novo_controlador_hotel.abre_tela()
            else:
                novo_controlador_hotel = ControladorHotel(hotel_entidade)
                self.__controladorasHoteis[nome_hotel] = novo_controlador_hotel
                novo_controlador_hotel.abre_tela()
        else:
            self.__tela.mostra_mensagem("Hotel não encontrado.")

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
                self.__tela.mostra_mensagem("Opção inválida.")
