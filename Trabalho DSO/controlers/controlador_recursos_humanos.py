from telas.tela_recursos_humanos import TelaRh
from controlers.controlador_cargo import ControladorCargo
from controlers.controlador_funcionario import ControladorFuncionario
from daos.rh_dao import RhDAO
from entidades.recursos_humanos import Rh


class ControladorRh:
    def __init__(
        self,
        controlador_cargo: ControladorCargo,
        controlador_funcionario: ControladorFuncionario
    ):
        self.__tela = TelaRh()
        self.__controlador_cargo = controlador_cargo
        self.__controlador_funcionario = controlador_funcionario
        self.__dao = RhDAO()

        rh_salvo = self.__dao.get()
        self.__rh = rh_salvo if rh_salvo else Rh()

    @property
    def rh(self) -> Rh:
        return self.__rh

    def salvar(self):
        """Salva alterações sempre que cargos ou funcionários mudam."""
        self.__dao.update(self.__rh)

    def menu_cargos(self):
        self.__controlador_cargo.abre_tela()
        self.salvar()

    def menu_funcionarios(self):
        if self.__controlador_cargo.get_quantidade_cargos() == 0:
            self.__tela.mostra_mensagem("Nenhum cargo cadastrado. Cadastre um cargo antes de cadastrar funcionário.")
            return
        
        self.__controlador_funcionario.abre_tela()
        self.salvar()

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando...")

    def abre_tela(self):
        opcoes = {
            1: self.menu_cargos,
            2: self.menu_funcionarios,
            0: self.retornar
        }

        while True:
            opcao = self.__tela.tela_opcoes()
            funcao = opcoes.get(opcao)

            if funcao:
                funcao()
                if opcao == 0:
                    break
            else:
                self.__tela.mostra_mensagem("Opção inválida.")
