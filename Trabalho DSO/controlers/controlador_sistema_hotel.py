from entidades.hotel import Hotel
from entidades.sistema_hotel import SistemaHotel
from controlers.controlador_hotel import ControladorHotel
from telas.tela_sistemahotel import TelaSistemaHotel
from daos.hotel_dao import HotelDAO
from daos.sistema_hotel_dao import SistemaHotelDAO


class ControladorSistemaHotel:

    def __init__(self, controlador_sistema=None):
        self.__hotel_DAO = HotelDAO()
        self.__tela = TelaSistemaHotel()
        self.__controlador_sistema = controlador_sistema
        self.__controladorasHoteis = {}

    def pega_hotel_por_nome(self, nome: str):
        nome = nome.strip().lower()
        for hotel in self.__hotel_DAO.get_all():
            if hotel.nome == nome:
                return hotel
        return None

    def incluir_hotel(self):
        dados = self.__tela.pega_dados_hotel()

        if not dados or not dados.get("nome"):
            self.__tela.mostra_mensagem("Dados inválidos.")
            return

        nome = dados["nome"].strip().lower()

        if self.pega_hotel_por_nome(nome):
            self.__tela.mostra_mensagem("Já existe um hotel com esse nome!")
            return

        hotel = Hotel(nome)
        self.__hotel_DAO.add(hotel)
        self.__tela.mostra_mensagem("Hotel incluído com sucesso.")

    def alterar_hotel(self):
        self.listar_hoteis()
        nome = self.__tela.seleciona_hotel()

        hotel = self.pega_hotel_por_nome(nome)
        if hotel is None:
            self.__tela.mostra_mensagem("Hotel não encontrado.")
            return

        novos_dados = self.__tela.pega_dados_hotel()
        if not novos_dados or not novos_dados.get("nome"):
            self.__tela.mostra_mensagem("Nome inválido.")
            return

        novo_nome = novos_dados["nome"].strip().lower()

        existente = self.pega_hotel_por_nome(novo_nome)
        if existente and existente != hotel:
            self.__tela.mostra_mensagem("Já existe outro hotel com esse nome.")
            return

        hotel.nome = novo_nome
        self.__hotel_DAO.update(hotel)
        self.__tela.mostra_mensagem("Hotel alterado com sucesso.")

    def excluir_hotel(self):
        self.listar_hoteis()
        nome = self.__tela.seleciona_hotel()

        hotel = self.pega_hotel_por_nome(nome)
        if hotel is None:
            self.__tela.mostra_mensagem("Hotel não encontrado.")
            return

        self.__hotel_DAO.remove(hotel.nome)
        self.__tela.mostra_mensagem("Hotel excluído com sucesso.")

    def listar_hoteis(self):
        dados_hoteis = []
        for hotel in self.__hotel_DAO.get_all():
            dados_hoteis.append({"nome": hotel.nome})

        if not dados_hoteis:
            self.__tela.mostra_mensagem("Nenhum hotel cadastrado.")
        else:
            self.__tela.mostra_lista(dados_hoteis)

    def acessar_hotel(self):
        self.listar_hoteis()
        nome = self.__tela.seleciona_hotel()

        hotel = self.pega_hotel_por_nome(nome)
        if hotel is None:
            self.__tela.mostra_mensagem("Hotel não encontrado.")
            return

        if hotel.nome in self.__controladorasHoteis:
            ctrl = self.__controladorasHoteis[hotel.nome]
        else:
            ctrl = ControladorHotel(hotel)
            self.__controladorasHoteis[hotel.nome] = ctrl

        ctrl.abre_tela()

    def retornar(self):
        if self.__controlador_sistema:
            self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes = {
            1: self.incluir_hotel,
            2: self.alterar_hotel,
            3: self.listar_hoteis,
            4: self.excluir_hotel,
            5: self.acessar_hotel,
            0: self.retornar
        }

        continua = True
        while continua:
            escolha = self.__tela.tela_opcoes()
            if escolha in opcoes:
                opcoes[escolha]()
            else:
                self.__tela.mostra_mensagem("Opção inválida.")
