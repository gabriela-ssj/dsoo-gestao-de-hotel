from entidades.cargo import Cargo
from telas.tela_cargo import TelaCargo
from typing import List, Optional

class ControladorCargo:
    def __init__(self):
        self.__tela = TelaCargo()
        self.__cargos: List[Cargo] = []
        self.populaCargos()

    def le_string(self, mensagem: str) -> str:
        print(mensagem, end="")
        return input() 

    def abre_tela(self):
        opcoes = {
            1: self.listar_cargos_disponiveis,
            2: self.criar_cargo,
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
                self.__tela.mostra_mensagem("Opção inválida.")
    
    def get_quantidade_cargos(self) -> int: 
        return len(self.__cargos)

    def buscar_cargo(self, tipo_cargo: str) -> Optional[Cargo]:
        for cargo in self.__cargos:
            if cargo.tipo_cargo.lower() == tipo_cargo.lower():
                return cargo
        return None

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")

    def listar_cargos_disponiveis(self):
        if not self.__cargos:
            self.__tela.mostra_mensagem("Nenhum cargo cadastrado.")
            return

        self.__tela.mostra_mensagem("--- LISTA DE CARGOS ---")
        lista_cargos_str = []
        for cargo in self.__cargos:
            
            lista_cargos_str.append(f"Tipo: {cargo.tipo_cargo.capitalize()} | Salário: R${cargo.salario_base:.2f}")
        self.__tela.mostra_lista(lista_cargos_str)


    def criar_cargo(self):
        dados = self.__tela.pega_dados_cargo()
        if dados is None:
            return

        nome_cargo = dados["nome"]
        salario = dados["salario"]

        if self.buscar_cargo(nome_cargo):
            self.__tela.mostra_mensagem(f"Cargo '{nome_cargo}' já existe.")
        else:
            try:
                novo_cargo = Cargo(tipo_cargo=nome_cargo, salario=salario)
                self.__cargos.append(novo_cargo)
                self.__tela.mostra_mensagem(f"Cargo '{nome_cargo}' criado com sucesso!")
            except ValueError as e:
                self.__tela.mostra_mensagem(f"Erro ao criar cargo: {e}")


    def alterar_cargo_via_tela(self):
        nome_cargo_para_alterar = self.__tela.seleciona_cargo()
        cargo_encontrado = self.buscar_cargo(nome_cargo_para_alterar)

        if cargo_encontrado:
            novos_dados = self.__tela.pega_dados_cargo(
                modo="alteracao",
                nome_atual=cargo_encontrado.tipo_cargo,
                salario_atual=cargo_encontrado.salario_base
            )
            if novos_dados is None:
                self.__tela.mostra_mensagem("Alteração de cargo cancelada.")
                return

            novo_nome = novos_dados["nome"]
            novo_salario = novos_dados["salario"]

            cargo_com_novo_nome = self.buscar_cargo(novo_nome)
            if cargo_com_novo_nome and cargo_com_novo_nome != cargo_encontrado:
                self.__tela.mostra_mensagem(f"Já existe um cargo com o nome '{novo_nome}'.")
                return

            try:
                cargo_encontrado.tipo_cargo = novo_nome 
                cargo_encontrado.salario_base = novo_salario 
                self.__tela.mostra_mensagem(f"Cargo alterado para '{novo_nome}'.")
            except ValueError as e:
                self.__tela.mostra_mensagem(f"Erro ao alterar cargo: {e}")
        else:
            self.__tela.mostra_mensagem("Cargo não encontrado.")

    def excluir_cargo_via_tela(self):
        nome_cargo_para_excluir = self.__tela.seleciona_cargo()
        cargo_encontrado = self.buscar_cargo(nome_cargo_para_excluir)

        if cargo_encontrado:
            confirmacao = self.__tela.le_string(f"Tem certeza que deseja excluir o cargo '{nome_cargo_para_excluir}'? (sim/nao): ").lower()
            if confirmacao == "sim":
                self.__cargos.remove(cargo_encontrado)
                self.__tela.mostra_mensagem(f"Cargo '{nome_cargo_para_excluir}' excluído.")
            else:
                self.__tela.mostra_mensagem("Operação de exclusão cancelada.")
        else:
            self.__tela.mostra_mensagem("Cargo não encontrado.")

    def buscar_cargo(self, tipo_cargo: str) -> Optional[Cargo]:
        for cargo in self.__cargos:
            if cargo.tipo_cargo.lower() == tipo_cargo.lower():
                return cargo
        return None

    def _adicionar_cargo_diretamente(self, nome: str, salario: float) -> bool:
        if not self.buscar_cargo(nome):
            try:
                novo_cargo = Cargo(tipo_cargo=nome, salario=salario)
                self.__cargos.append(novo_cargo)
                return True
            except ValueError as e:
                print(f"Erro interno ao popular cargo '{nome}': {e}") # Loga o erro, não exibe na tela
                return False
        return False

    def populaCargos(self):
        cargos_iniciais = [
            ("gerente", 5000.0),
            ("recepcionista", 2500.0),
            ("camareira", 2200.0),
            ("cozinheira", 2300.0),
            ("limpeza", 2000.0),
            ("servicosgerais", 2100.0),
        ]
        for nome, salario in cargos_iniciais:
            self._adicionar_cargo_diretamente(nome, salario)
