from entidades.funcionario import Funcionario
from telas.tela_funcionario import TelaFuncionario

class ControladorFuncionario:
    def __init__(self, controlador_cargo):
        self.__funcionarios = []
        self.__controlador_cargo = controlador_cargo
        self.__tela = TelaFuncionario()
        self.__retorno_callback = None

    def set_retorno_callback(self, callback):
        self.__retorno_callback = callback

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
        if self.__retorno_callback:
            self.__retorno_callback()
        else:
            self.__tela.mostra_mensagem("Retornando...")

    def cadastrar_funcionario(self):
        dados = self.__tela.pega_dados_funcionario()
        cargo = self.__controlador_cargo.buscar_cargo(dados["tipo_cargo"])

        if not cargo:
            self.__tela.mostra_mensagem(
                f"⚠️ Cargo '{dados['tipo_cargo']}' não encontrado. Cadastre o cargo antes de continuar."
            )
            return

        try:
            funcionario = Funcionario(
                nome=dados["nome"],
                cpf=dados["cpf"],
                telefone=dados["telefone"],
                idade=int(dados["idade"]),
                email=dados["email"],
                cargo=cargo
            )
            self.__funcionarios.append(funcionario)
            self.__tela.mostra_mensagem(f"✅ Funcionário {funcionario.nome} cadastrado com sucesso!")
        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro ao cadastrar funcionário: {e}")

    def listar_funcionarios(self):
        if not self.__funcionarios:
            self.__tela.mostra_mensagem("Nenhum funcionário cadastrado.")
            return
        lista = [
            f"- {f.nome} | Cargo: {f.cargo.tipo_cargo.capitalize()} | CPF: {f.cpf}"
            for f in self.__funcionarios
        ]
        self.__tela.mostra_lista(lista)

    def excluir_funcionario(self):
        cpf = self.__tela.seleciona_funcionario()
        funcionario = self.buscar_funcionario_por_cpf(cpf)
        if funcionario:
            self.__funcionarios.remove(funcionario)
            self.__tela.mostra_mensagem(f"✅ Funcionário com CPF {cpf} excluído.")
        else:
            self.__tela.mostra_mensagem(f"⚠️ Funcionário com CPF {cpf} não encontrado.")

    def alterar_funcionario(self):
        cpf = self.__tela.seleciona_funcionario()
        funcionario = self.buscar_funcionario_por_cpf(cpf)
        if funcionario:
            novos_dados = self.__tela.pega_dados_funcionario()
            novo_cargo = self.__controlador_cargo.buscar_cargo(novos_dados["tipo_cargo"])
            if not novo_cargo:
                self.__tela.mostra_mensagem(
                    f"⚠️ Cargo '{novos_dados['tipo_cargo']}' não encontrado. Cadastre o cargo antes de continuar."
                )
                return

            funcionario.nome = novos_dados["nome"]
            funcionario.cpf = novos_dados["cpf"]
            funcionario.idade = int(novos_dados["idade"])
            funcionario.telefone = novos_dados["telefone"]
            funcionario.email = novos_dados["email"]
            funcionario.cargo = novo_cargo
            self.__tela.mostra_mensagem("✅ Funcionário alterado com sucesso.")
        else:
            self.__tela.mostra_mensagem("⚠️ Funcionário não encontrado.")

    def buscar_funcionario_por_cpf(self, cpf):
        return next((f for f in self.__funcionarios if f.cpf == cpf), None)
