from entidades.cargo import Cargo
from telas.tela_cargo import TelaCargo

class ControladorCargo:
    def __init__(self):
        self.__cargos = []
        self.__tela = TelaCargo()

    @property
    def cargos(self):
        return self.__cargos

    def abre_tela(self):
        opcoes = {
            1: self.listar_cargos_disponiveis,
            2: self.criar_cargo_via_tela,
            3: self.alterar_cargo_via_tela,
            4: self.excluir_cargo_via_tela,
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

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando...")

    def listar_cargos_disponiveis(self):
        if not self.__cargos:
            self.__tela.mostra_mensagem("Nenhum cargo cadastrado.")
        else:
            lista = [c.tipo_cargo for c in self.__cargos]
            self.__tela.mostra_lista(lista)

    def criar_cargo_via_tela(self):
        tipo_cargo = self.__tela.pega_dados_cargo()
        self.criar_cargo(tipo_cargo)

    def criar_cargo(self, tipo_cargo: str) -> Cargo:
        if self.buscar_cargo(tipo_cargo):
            self.__tela.mostra_mensagem(f"⚠️ Cargo '{tipo_cargo}' já existe.")
            return None
        try:
            cargo = Cargo(tipo_cargo)
            self.__cargos.append(cargo)
            self.__tela.mostra_mensagem(f"✅ Cargo '{tipo_cargo}' criado com sucesso!")
            return cargo
        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")
            return None

    def alterar_cargo_via_tela(self):
        nome_atual = self.__tela.seleciona_cargo()
        cargo = self.buscar_cargo(nome_atual)
        if cargo:
            novo_nome = self.__tela.pega_dados_cargo()
            if self.buscar_cargo(novo_nome):
                self.__tela.mostra_mensagem(f"⚠️ Cargo '{novo_nome}' já existe.")
            else:
                cargo.tipo_cargo = novo_nome
                self.__tela.mostra_mensagem(f"✅ Cargo alterado para '{novo_nome}'.")
        else:
            self.__tela.mostra_mensagem("⚠️ Cargo não encontrado.")

    def excluir_cargo_via_tela(self):
        nome = self.__tela.seleciona_cargo()
        cargo = self.buscar_cargo(nome)
        if cargo:
            self.__cargos.remove(cargo)
            self.__tela.mostra_mensagem(f"✅ Cargo '{nome}' excluído.")
        else:
            self.__tela.mostra_mensagem("⚠️ Cargo não encontrado.")

    def buscar_cargo(self, tipo_cargo: str):
        for cargo in self.__cargos:
            if cargo.tipo_cargo == tipo_cargo.lower():
                return cargo
        return None
