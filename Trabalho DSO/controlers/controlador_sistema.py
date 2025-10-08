from telas.tela_sistema import TelaSistema
from controlers.controlador_sistema_hotel import ControladorSistemaHotel
from controlers.controlador_hospede import ControladorHospede
from controlers.controlador_pet import ControladorPet
from controlers.controlador_funcionario import ControladorFuncionario
from controlers.controlador_cargo import ControladorCargo

class ControladorSistema:
    def __init__(self):
        self.__tela = TelaSistema()

        self.controlador_hospede = ControladorHospede()
        self.controlador_pet = ControladorPet(self.controlador_hospede)
        self.controlador_cargo = ControladorCargo()
        self.controlador_funcionario = ControladorFuncionario()
        self.__controlador_sistema_hotel = ControladorSistemaHotel(self)

    def inicializa_sistema(self):
        self.abre_tela()

    def gerenciar_hoteis(self):
        self.__controlador_sistema_hotel.abre_tela()

    def encerra_sistema(self):
        self.__tela.mostra_mensagem("Encerrando o sistema...")
        exit(0)

    def abre_tela(self):
        opcoes = {
            1: self.gerenciar_hoteis,
            0: self.encerra_sistema
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
            else:
                self.__tela.mostra_mensagem("Opção inválida.")
