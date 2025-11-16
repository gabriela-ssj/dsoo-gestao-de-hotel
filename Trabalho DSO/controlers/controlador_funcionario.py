from entidades.funcionario import Funcionario
from controlers.controlador_cargo import ControladorCargo
from telas.tela_funcionario import TelaFuncionario
from controlers.ValidacaoException import ValidacaoException


class ControladorFuncionario:

    def __init__(self, controlador_cargo: ControladorCargo):
        self.__funcionarios = []
        self.__controlador_cargo = controlador_cargo
        self.__tela = TelaFuncionario()

    @property
    def funcionarios(self):
        return self.__funcionarios


    def abre_tela(self):
        opcoes = {
            1: self.cadastrar_funcionario,
            2: self.listar_funcionarios,
            3: self.excluir_funcionario,
            4: self.alterar_funcionario,
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


    def cadastrar_funcionario(self):
        try:
            dados = self.__tela.pega_dados_funcionario()
            ValidacaoException.se_none(dados, "Dados não fornecidos.")

            ValidacaoException.validar_campo_vazio(dados["nome"], "nome")
            ValidacaoException.validar_cpf_unico(self.__funcionarios, dados["cpf"])
            ValidacaoException.validar_idade_valida(int(dados["idade"]))
            ValidacaoException.validar_email(dados["email"])

            cargo = self.__controlador_cargo.buscar_cargo(dados["tipo_cargo"])
            if not cargo:
                self.__tela.mostra_mensagem(
                    f"⚠️ Cargo '{dados['tipo_cargo']}' não encontrado. Criando automaticamente..."
                )
                cargo = self.__controlador_cargo.criar_cargo(
                    dados["tipo_cargo"], 0
                )

            funcionario = Funcionario(
                nome=dados["nome"],
                cpf=dados["cpf"],
                idade=int(dados["idade"]),
                telefone=dados["telefone"],
                email=dados["email"],
                cargo=cargo
            )

            self.__funcionarios.append(funcionario)
            self.__tela.mostra_mensagem(f"✅ Funcionário {funcionario.nome} cadastrado com sucesso!")

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"⚠️ Erro: {e}")

    def listar_funcionarios(self):
        try:
            ValidacaoException.se_vazio(
                self.__funcionarios,
                "Nenhum funcionário cadastrado."
            )

            lista = [
                f"- {f.nome} | {f.cargo._tipo_cargo.capitalize()} | CPF: {f.cpf}"
                for f in self.__funcionarios
            ]
            self.__tela.mostra_lista(lista)

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"⚠️ {e}")

    def excluir_funcionario(self):
        cpf = self.__tela.seleciona_funcionario()
        antes = len(self.__funcionarios)

        self.__funcionarios = [
            f for f in self.__funcionarios if f.cpf != cpf
        ]

        if len(self.__funcionarios) < antes:
            self.__tela.mostra_mensagem(f"🗑️ Funcionário {cpf} excluído.")
        else:
            self.__tela.mostra_mensagem("⚠️ Funcionário não encontrado.")

    def alterar_funcionario(self):
        try:
            funcionario = self.buscar_funcionario()
            ValidacaoException.se_none(funcionario, "Funcionário não encontrado.")

            novos = self.__tela.pega_dados_funcionario()

            ValidacaoException.validar_idade_valida(int(novos["idade"]))
            ValidacaoException.validar_email(novos["email"])

            cargo = self.__controlador_cargo.buscar_cargo(novos["tipo_cargo"])
            if not cargo:
                self.__tela.mostra_mensagem(
                    f"⚠️ Cargo '{novos['tipo_cargo']}' não encontrado. Criando automaticamente..."
                )
                cargo = self.__controlador_cargo.criar_cargo(novos["tipo_cargo"], 0)

            funcionario.nome = novos["nome"]
            funcionario.cpf = novos["cpf"]
            funcionario.idade = int(novos["idade"])
            funcionario.telefone = novos["telefone"]
            funcionario.email = novos["email"]
            funcionario.cargo = cargo

            self.__tela.mostra_mensagem("✅ Funcionário alterado com sucesso!")

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"⚠️ {e}")


    def buscar_funcionario(self, cpf: str = None):
        if not cpf:
            cpf = self.__tela.seleciona_funcionario()

        for f in self.__funcionarios:
            if f.cpf == cpf:
                return f

        return None
