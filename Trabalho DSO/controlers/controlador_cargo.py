from entidades.cargo import Cargo
from telas.tela_cargo import TelaCargo

class ControladorCargo:
    def __init__(self):
        self.__cargos = []
        self.__tela = TelaCargo()

    @property
    def cargos(self):
        return self.__cargos

    def listar_cargos_disponiveis(self):
        if not self.__cargos:
            self.__tela.mostra_mensagem("Nenhum cargo cadastrado.")
        else:
            lista = [c.tipo_cargo for c in self.__cargos]
            self.__tela.mostra_lista(lista)

    def criar_cargo(self, tipo_cargo: str) -> Cargo:
        try:
            cargo = Cargo(tipo_cargo)
            self.__cargos.append(cargo)
            self.__tela.mostra_mensagem(f"Cargo '{tipo_cargo}' criado com sucesso!")
            return cargo
        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")
            return None

    def buscar_cargo(self, tipo_cargo: str):
        for cargo in self.__cargos:
            if cargo.tipo_cargo == tipo_cargo.lower():
                return cargo
        return None