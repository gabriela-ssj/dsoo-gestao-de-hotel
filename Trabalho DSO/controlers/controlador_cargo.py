# controlers\controlador_cargo.py
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
            9: self.populaCargos, # Manter para testes
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

    def get_quantidade_cargos(self):
        return len(self.cargos)

    def listar_cargos_disponiveis(self):
        if not self.get_quantidade_cargos():
            self.__tela.mostra_mensagem("Nenhum cargo cadastrado.")
        else:
            lista = [f"Tipo: {c.tipo_cargo[0].capitalize()} | Salário: R${c.tipo_cargo[1]:.2f}" for c in self.__cargos]
            self.__tela.mostra_lista(lista)

    def criar_cargo_via_tela(self):
        dados = self.__tela.pega_dados_cargo()
        if dados:
            self.criar_cargo(dados["nome"], dados["salario"])

    def criar_cargo(self, tipo_cargo: str, salario: float = 0) -> Cargo:
        cargo = self.buscar_cargo(tipo_cargo)
        if cargo:
            self.__tela.mostra_mensagem(f"⚠️ Cargo '{tipo_cargo}' já existe.")
            return None
        try:
            cargo = Cargo(tipo_cargo,salario)
            self.__cargos.append(cargo)
            self.__tela.mostra_mensagem(f"✅ Cargo '{tipo_cargo}' criado com sucesso!")
        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")
            return None
        return cargo

    def alterar_cargo_via_tela(self):
        nome_atual = self.__tela.seleciona_cargo()
        cargo = self.buscar_cargo(nome_atual)
        if cargo:
            dados = self.__tela.pega_dados_cargo()
            if dados:
                novo_nome = dados["nome"]
                salario = dados["salario"]
                if self.buscar_cargo(novo_nome) and novo_nome.lower() != nome_atual.lower():
                    self.__tela.mostra_mensagem(f"⚠️ Cargo '{novo_nome}' já existe.")
                else:
                    cargo.tipo_cargo = novo_nome
                    cargo.salario_base = salario
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
            if cargo.tipo_cargo[0].lower() == tipo_cargo.lower():
                return cargo
        return None

    # Facilitar testes
    def populaCargos(self):
        cargos = [
            ("gerente", 5000.0),
            ("recepcionista", 2500.0),
            ("camareira", 2200.0),
            ("cozinheira", 2300.0),
            ("limpeza", 2000.0),
            ("serviçosgerais", 2100.0),
        ]
        for cargo in cargos:
            if not self.buscar_cargo(cargo[0]):
                self.criar_cargo(cargo[0], cargo[1])
            else:
                self.__tela.mostra_mensagem(f"Cargo '{cargo[0]}' já existe e não foi recriado.")