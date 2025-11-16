from entidades.funcionario import Funcionario
from controlers.controlador_cargo import ControladorCargo
from telas.tela_funcionario import TelaFuncionario


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
            if dados is None:
                return

            if not self.__controlador_cargo.buscar_cargo(dados["tipo_cargo"]):
                self.__tela.mostra_mensagem(
                    f"⚠️ Cargo '{dados['tipo_cargo']}' ainda não está cadastrado. Criando automaticamente..."
                )
                self.__controlador_cargo.criar_cargo(dados["tipo_cargo"], 0)

            cargo = self.__controlador_cargo.buscar_cargo(dados["tipo_cargo"])

            funcionario = Funcionario(
                nome=dados["nome"],
                cpf=dados["cpf"],
                idade=int(dados["idade"]),
                telefone=dados["telefone"],
                email=dados["email"],
                cargo=cargo
            )

            self.__funcionarios.append(funcionario)
            self.__tela.mostra_mensagem(
                f"✅ Funcionário {funcionario.nome} ({funcionario.cargo}) cadastrado com sucesso!"
            )

        except ValueError:
            self.__tela.mostra_mensagem("❌ Idade inválida: digite apenas números.")
        except Exception as e:
            self.__tela.mostra_mensagem(f"❌ Erro inesperado ao cadastrar: {e}")


    def listar_funcionarios(self):
        if not self.__funcionarios:
            self.__tela.mostra_mensagem("Nenhum funcionário cadastrado.")
            return

        lista = [
            f"- {f.nome} | {f.cargo._tipo_cargo.capitalize()} | CPF: {f.cpf}"
            for f in self.__funcionarios
        ]
        self.__tela.mostra_lista(lista)


    def excluir_funcionario(self):
        cpf = self.__tela.seleciona_funcionario()

        antes = len(self.__funcionarios)
        self.__funcionarios = [f for f in self.__funcionarios if f.cpf != cpf]

        if len(self.__funcionarios) < antes:
            self.__tela.mostra_mensagem(f"✅ Funcionário com CPF {cpf} excluído.")
        else:
            self.__tela.mostra_mensagem(f"⚠️ Nenhum funcionário com CPF {cpf} encontrado.")


    def alterar_funcionario(self):
        funcionario = self.buscar_funcionario()
        if not funcionario:
            self.__tela.mostra_mensagem("⚠️ Funcionário não encontrado.")
            return

        try:
            novos_dados = self.__tela.pega_dados_funcionario()
            if novos_dados is None:
                return

            novo_cargo = self.__controlador_cargo.buscar_cargo(novos_dados["tipo_cargo"])
            if not novo_cargo:
                self.__tela.mostra_mensagem(
                    f"⚠️ Cargo '{novos_dados['tipo_cargo']}' não cadastrado. Criando automaticamente..."
                )
                novo_cargo = self.__controlador_cargo.criar_cargo(novos_dados["tipo_cargo"])

            funcionario.nome = novos_dados["nome"]
            funcionario.cpf = novos_dados["cpf"]
            funcionario.idade = int(novos_dados["idade"])
            funcionario.telefone = novos_dados["telefone"]
            funcionario.email = novos_dados["email"]
            funcionario.cargo = novo_cargo

            self.__tela.mostra_mensagem("✅ Funcionário alterado com sucesso.")

        except ValueError:
            self.__tela.mostra_mensagem("❌ Idade inválida: digite apenas números.")
        except Exception as e:
            self.__tela.mostra_mensagem(f"❌ Erro inesperado ao alterar: {e}")


    def buscar_funcionario(self, cpf: str = None):
        if not cpf:
            cpf = self.__tela.seleciona_funcionario()

        for funcionario in self.__funcionarios:
            if funcionario.cpf == cpf:
                return funcionario

        return None
