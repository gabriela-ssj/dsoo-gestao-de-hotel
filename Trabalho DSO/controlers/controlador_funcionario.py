from entidades.funcionario import Funcionario
from controlers.controlador_cargo import ControladorCargo
from telas.tela_recursos_humanos import TelaRh

class ControladorFuncionario:
    def __init__(self, rh=None):
        self.__funcionarios = []
        self.__controlador_cargo = ControladorCargo()
        self.__rh = rh
        self.__tela = TelaRh()

    @property
    def funcionarios(self):
        return self.__funcionarios

    def cadastrar_funcionario(self):
        dados = self.__tela.pega_dados_funcionario()

        if not self.__controlador_cargo.buscar_cargo(dados["tipo_cargo"]):
            self.__tela.mostra_mensagem(
                f"⚠️ Cargo '{dados['tipo_cargo']}' ainda não está cadastrado. Criando automaticamente..."
            )
            self.__controlador_cargo.criar_cargo(dados["tipo_cargo"])

        try:
            funcionario = Funcionario(
                nome=dados["nome"],
                cpf=dados["cpf"],
                telefone=dados["telefone"],
                idade=dados["idade"],
                email=dados["email"],
                cargo=dados["tipo_cargo"]
            )
            self.__funcionarios.append(funcionario)
            self.__tela.mostra_mensagem(f"Funcionário {funcionario.nome} ({funcionario.cargo}) cadastrado com sucesso!")
        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro ao cadastrar funcionário: {e}")

    def listar_funcionarios(self):
        if not self.__funcionarios:
            self.__tela.mostra_mensagem("Nenhum funcionário cadastrado.")
            return
        lista = [f"- {f.nome} | {f.cargo.capitalize()} | CPF: {f.cpf}" for f in self.__funcionarios]
        self.__tela.mostra_lista(lista)

    def excluir_funcionario(self):
        cpf = self.__tela.seleciona_funcionario()
        antes = len(self.__funcionarios)
        self.__funcionarios = [f for f in self.__funcionarios if f.cpf != cpf]
        if len(self.__funcionarios) < antes:
            self.__tela.mostra_mensagem(f"Funcionário com CPF {cpf} excluído.")
        else:
            self.__tela.mostra_mensagem(f"Nenhum funcionário com CPF {cpf} encontrado.")

    def buscar_funcionario(self, cpf: str):
        for f in self.__funcionarios:
            if f.cpf == cpf:
                return f
        return None
