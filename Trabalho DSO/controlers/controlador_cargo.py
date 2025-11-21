from entidades.cargo import Cargo
from telas.tela_cargo import TelaCargo
from typing import Optional, Dict, Any, List
from controlers.ValidacaoException import ValidacaoException
from daos.cargo_dao import CargoDAO

class ControladorCargo:
    def __init__(self):
        self.__tela = TelaCargo()
        self.__cargo_dao = CargoDAO()
        self.populaCargos()

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

            funcao_escolhida = opcoes.get(opcao)

            if funcao_escolhida:
                if opcao == 0:
                    break
                funcao_escolhida()
            else:
                self.__tela.mostra_mensagem("Opção inválida.")

    def get_quantidade_cargos(self) -> int:
        return len(self.__cargo_dao.get_all())

    def buscar_cargo(self, tipo_cargo: str) -> Optional[Cargo]:
        return self.__cargo_dao.get(tipo_cargo)

    def retornar(self):
        pass

    def listar_cargos_disponiveis(self):
        cargos = list(self.__cargo_dao.get_all().values())

        if not cargos:
            self.__tela.mostra_mensagem("Nenhum cargo cadastrado.")
            return

        dados_cargos = [{"nome": c.tipo_cargo.capitalize(), "salario": c.salario_base} for c in cargos]
        self.__tela.mostra_lista(dados_cargos)

    def criar_cargo_via_tela(self):
        dados = self.__tela.pega_dados_cargo(modo="cadastro")
        if dados is None:
            return

        nome_cargo = dados["nome"]
        salario = dados["salario"]

        try:
            self.adicionar_cargo_programaticamente(nome_cargo, salario)
            self.__tela.mostra_mensagem(f"Cargo '{nome_cargo.capitalize()}' criado com sucesso!")
        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"Erro ao criar cargo: {e}")

    def adicionar_cargo_programaticamente(self, tipo_cargo: str, salario: float) -> Cargo:
        if not tipo_cargo.strip():
            raise ValidacaoException("Tipo de cargo deve ser uma string não vazia.")

        if self.buscar_cargo(tipo_cargo):
            raise ValidacaoException(f"Cargo '{tipo_cargo.capitalize()}' já existe.")

        novo_cargo = Cargo(tipo_cargo=tipo_cargo, salario_base=salario)
        self.__cargo_dao.add(novo_cargo)
        return novo_cargo

    def alterar_cargo_via_tela(self):
        nome_cargo_para_alterar = self.__tela.seleciona_cargo()
        if not nome_cargo_para_alterar:
            self.__tela.mostra_mensagem("Alteração de cargo cancelada.")
            return

        cargo_encontrado = self.buscar_cargo(nome_cargo_para_alterar)

        if cargo_encontrado:
            novos_dados = self.__tela.pega_dados_cargo(
                modo="alteracao",
                nome_atual=cargo_encontrado.tipo_cargo.capitalize(),
                salario_atual=cargo_encontrado.salario_base
            )

            if novos_dados is None:
                self.__tela.mostra_mensagem("Alteração cancelada.")
                return

            novo_nome = novos_dados["nome"]
            novo_salario = novos_dados["salario"]

            if novo_nome.lower() != cargo_encontrado.tipo_cargo.lower():
                if self.buscar_cargo(novo_nome):
                    self.__tela.mostra_mensagem(f"Já existe um cargo '{novo_nome.capitalize()}'.")
                    return

                self.__cargo_dao.remove(cargo_encontrado.tipo_cargo)
                cargo_encontrado.tipo_cargo = novo_nome

            cargo_encontrado.salario_base = novo_salario

            self.__cargo_dao.update(cargo_encontrado)

            self.__tela.mostra_mensagem(
                f"Cargo alterado para '{cargo_encontrado.tipo_cargo.capitalize()}' (R${cargo_encontrado.salario_base:.2f})."
            )
        else:
            self.__tela.mostra_mensagem(f"Cargo '{nome_cargo_para_alterar}' não encontrado.")

    def excluir_cargo_via_tela(self):
        nome = self.__tela.seleciona_cargo()

        if not nome:
            self.__tela.mostra_mensagem("Exclusão cancelada.")
            return

        cargo = self.buscar_cargo(nome)
        if not cargo:
            self.__tela.mostra_mensagem(f"Cargo '{nome}' não encontrado.")
            return

        confirmacao = self.__tela.confirma_acao(
            f"Tem certeza que deseja excluir o cargo '{nome.capitalize()}'?"
        )

        if confirmacao:
            self.__cargo_dao.remove(nome)
            self.__tela.mostra_mensagem(f"Cargo '{nome.capitalize()}' excluído.")
        else:
            self.__tela.mostra_mensagem("Operação cancelada.")

    def populaCargos(self):
        if len(self.__cargo_dao.get_all()) > 0:
            return  

        cargos_iniciais = [
            ("gerente", 5000.0),
            ("recepcionista", 2500.0),
            ("camareira", 2200.0),
            ("cozinheira", 2300.0),
            ("limpeza", 2000.0),
            ("serviços gerais", 2100.0),
        ]

        for nome, salario in cargos_iniciais:
            try:
                self.adicionar_cargo_programaticamente(nome, salario)
            except:
                pass
