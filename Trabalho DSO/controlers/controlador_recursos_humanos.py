from entidades.recursos_humanos import Rh
from telas.tela_recursos_humanos import TelaRh
from controlers.controlador_cargo import ControladorCargo
from controlers.controlador_funcionario import ControladorFuncionario

class ControladorRh:
    def __init__(self):
        self.__tela = TelaRh()
        self.__controlador_cargo = ControladorCargo()
        self.__controlador_funcionario = ControladorFuncionario()
        self.__retorno_callback = None  

    def set_retorno_callback(self, callback):
        self.__retorno_callback = callback

    def menu_cargos(self):
        self.__controlador_cargo.abre_tela()

    def menu_funcionarios(self):
        if not self.__controlador_cargo.get_quantidade_cargos():
            self.__tela.mostra_mensagem("Nenhum cargo cadastrado. Cadastre um cargo antes de incluir funcionários.")
            return
        self.__controlador_funcionario.abre_tela()

    def retornar(self):
        if self.__retorno_callback:
            self.__retorno_callback()
        else:
            self.__tela.mostra_mensagem("Retornando ao menu anterior...")

    def abre_tela(self):
        opcoes = {
            1: self.menu_cargos,
            2: self.menu_funcionarios,
            0: self.retornar
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
                if opcao == 0:
                    break
            else:
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")
