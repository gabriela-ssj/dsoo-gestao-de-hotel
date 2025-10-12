from entidades.cargo import Cargo
from telas.tela_cargo import TelaCargo
from typing import List, Optional

class ControladorCargo:
    def __init__(self):
        self.__cargos: List[Cargo] = []
        self.__tela = TelaCargo()

    @property
    def cargos(self) -> List[Cargo]:
        return self.__cargos.copy()

    def abre_tela(self):
        opcoes = {
            1: self.listar_cargos_disponiveis,
            2: self.criar_cargo_via_tela,
            3: self.alterar_cargo_via_tela,
            4: self.excluir_cargo_via_tela,
            9: self.popula_cargos,
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

    def get_quantidade_cargos(self) -> int:
        return len(self.__cargos)

    def listar_cargos_disponiveis(self):
        if not self.__cargos:
            self.__tela.mostra_mensagem("Nenhum cargo cadastrado.")
        else:
            lista = [f"{c.tipo_cargo.capitalize()} - R$ {c.salario_base:.2f}" for c in self.__cargos]
            self.__tela.mostra_lista(lista)

    def criar_cargo_via_tela(self):
        dados = self.__tela.pega_dados_cargo()
        self.criar_cargo(dados["nome"], dados["salario"])

    def criar_cargo(self, tipo_cargo: str, salario: float = 0) -> Optional[Cargo]:
        if self.buscar_cargo(tipo_cargo):
            self.__tela.mostra_mensagem(f"⚠️ Cargo '{tipo_cargo}' já existe.")
            return None
        try:
            cargo = Cargo(tipo_cargo, salario)
            self.__cargos.append(cargo)
            self.__tela.mostra_mensagem(f"✅ Cargo '{tipo_cargo}' criado com sucesso!")
            return cargo
        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")
            return None

    def alterar_cargo_via_tela(self):
        nome_atual = self.__tela.seleciona_cargo()
        cargo = self.buscar_cargo(nome_atual)
        if not cargo:
            self.__tela.mostra_mensagem("⚠️ Cargo não encontrado.")
            return

        dados = self.__tela.pega_dados_cargo()
        novo_nome = dados["nome"]
        novo_salario = dados["salario"]

        if novo_nome != nome_atual and self.buscar_cargo(novo_nome):
            self.__tela.mostra_mensagem(f"⚠️ Cargo '{novo_nome}' já existe.")
            return

        cargo.tipo_cargo = novo_nome
        cargo._salario_base = novo_salario  # Pode ser ajustado para setter se existir
        self.__tela.mostra_mensagem(f"✅ Cargo alterado para '{novo_nome}'.")

    def excluir_cargo_via_tela(self):
        nome = self.__tela.seleciona_cargo()
        cargo = self.buscar_cargo(nome)
        if cargo:
            self.__cargos.remove(cargo)
            self.__tela.mostra_mensagem(f"✅ Cargo '{nome}' excluído.")
        else:
            self.__tela.mostra_mensagem("⚠️ Cargo não encontrado.")

    def buscar_cargo(self, tipo_cargo: str) -> Optional[Cargo]:
        tipo_cargo = tipo_cargo.lower()
        for cargo in self.__cargos:
            if cargo.tipo_cargo == tipo_cargo:
                return cargo
        return None

    def popula_cargos(self):
        cargos = [
            ("gerente", 5000.0),
            ("recepcionista", 2500.0),
            ("camareira", 2200.0),
            ("cozinheira", 2300.0),
            ("limpeza", 2000.0),
            ("serviçosgerais", 2100.0),
        ]
        for nome, salario in cargos:
            self.criar_cargo(nome, salario)
