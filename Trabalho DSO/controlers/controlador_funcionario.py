from entidades.funcionario import Funcionario
from entidades.cargo import Cargo
from telas.tela_funcionario import TelaFuncionario
from controlers.controlador_cargo import ControladorCargo
from controlers.ValidacaoException import ValidacaoException
from typing import Optional, Dict, Any, List
from daos.funcionario_dao import FuncionarioDAO


class ControladorFuncionario:
    def __init__(self, controlador_cargo: ControladorCargo):
        if not isinstance(controlador_cargo, ControladorCargo):
            raise TypeError("ControladorFuncionario deve ser inicializado com um objeto ControladorCargo.")

        self.__dao = FuncionarioDAO()
        self.__controlador_cargo = controlador_cargo
        self.__tela = TelaFuncionario()

    @property
    def funcionarios(self) -> List[Funcionario]:
        return list(self.__dao.get_all().values())

    def abre_tela(self):
        opcoes = {
            '1': self.cadastrar_funcionario,
            '2': self.listar_funcionarios,
            '3': self.alterar_funcionario,
            '4': self.excluir_funcionario,
            '0': self.retornar
        }

        while True:
            opcao = self.__tela.tela_opcoes()

            funcao_escolhida = opcoes.get(str(opcao))
            if funcao_escolhida:
                if opcao == 0:
                    break
                funcao_escolhida()
            else:
                self.__tela.mostra_mensagem("Opção inválida.")

    def retornar(self):
        pass

    def _buscar_funcionario_por_cpf(self, cpf: str) -> Funcionario:
        funcionario = self.__dao.get(cpf)
        if not funcionario:
            raise ValidacaoException(f"Funcionário com CPF {cpf} não encontrado.")
        return funcionario

    def cadastrar_funcionario(self):
        try:
            dados = self.__tela.pega_dados_funcionario(modo="cadastro")

            ValidacaoException.se_none(dados, "Operação cancelada.")
            ValidacaoException.validar_cpf_unico(self.funcionarios, dados["cpf"])
            ValidacaoException.validar_campo_vazio(dados["nome"], "nome")
            ValidacaoException.validar_idade_valida(int(dados["idade"]))
            ValidacaoException.validar_email(dados["email"])
            ValidacaoException.validar_salario_valido(float(dados["salario"]))

            cargo = self.__controlador_cargo.buscar_cargo(dados["tipo_cargo"])
            if not cargo:
                salario_padrao = self.__controlador_cargo.get_default_salario_for_cargo(dados["tipo_cargo"])
                cargo = self.__controlador_cargo.adicionar_cargo_programaticamente(
                    dados["tipo_cargo"], salario_padrao
                )

            funcionario = Funcionario(
                nome=dados["nome"],
                cpf=dados["cpf"],
                idade=int(dados["idade"]),
                telefone=dados["telefone"],
                email=dados["email"],
                cargo=cargo,
                salario=float(dados["salario"])
            )

            self.__dao.add(funcionario)
            self.__tela.mostra_mensagem(f"Funcionário {funcionario.nome} cadastrado com sucesso!")

        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro ao cadastrar funcionário: {e}")


    def listar_funcionarios(self):
        funcionarios = self.funcionarios

        if not funcionarios:
            self.__tela.mostra_mensagem("Nenhum funcionário cadastrado.")
            return

        dados = [f.to_dict() for f in funcionarios]
        self.__tela.mostra_funcionarios(dados)


    def alterar_funcionario(self):
        try:
            cpf = self.__tela.seleciona_funcionario()
            ValidacaoException.se_none(cpf, "Operação cancelada.")

            funcionario = self._buscar_funcionario_por_cpf(cpf)

            novos_dados = self.__tela.pega_dados_funcionario(
                modo="alteracao",
                dados_atuais=funcionario.to_dict()
            )
            ValidacaoException.se_none(novos_dados, "Operação cancelada.")

            ValidacaoException.validar_campo_vazio(novos_dados["nome"], "nome")
            ValidacaoException.validar_idade_valida(int(novos_dados["idade"]))
            ValidacaoException.validar_email(novos_dados["email"])
            ValidacaoException.validar_salario_valido(float(novos_dados["salario"]))

            cargo_atual = funcionario.cargo
            novo_cargo = cargo_atual

            if novos_dados["tipo_cargo"].lower() != cargo_atual.tipo_cargo.lower():
                novo_cargo = self.__controlador_cargo.buscar_cargo(novos_dados["tipo_cargo"])
                if not novo_cargo:
                    salario_padrao = self.__controlador_cargo.get_default_salario_for_cargo(
                        novos_dados["tipo_cargo"]
                    )
                    novo_cargo = self.__controlador_cargo.adicionar_cargo_programaticamente(
                        novos_dados["tipo_cargo"], salario_padrao
                    )

            funcionario.nome = novos_dados["nome"]
            funcionario.idade = int(novos_dados["idade"])
            funcionario.telefone = novos_dados["telefone"]
            funcionario.email = novos_dados["email"]
            funcionario.salario = float(novos_dados["salario"])
            funcionario.cargo = novo_cargo

            self.__dao.update(funcionario)
            self.__tela.mostra_mensagem("Funcionário alterado com sucesso!")

        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro ao alterar funcionário: {e}")

    def excluir_funcionario(self):
        try:
            cpf = self.__tela.seleciona_funcionario()
            ValidacaoException.se_none(cpf, "Operação cancelada.")

            funcionario = self._buscar_funcionario_por_cpf(cpf)

            if self.__tela.confirma_acao(f"Deseja excluir {funcionario.nome}?"):
                self.__dao.remove(cpf)
                self.__tela.mostra_mensagem("Funcionário removido!")

        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro ao excluir funcionário: {e}")

    def buscar_funcionario(self, cpf: str):
        return self.__dao.get(cpf)
