from entidades.recursos_humanos import Rh
from entidades.funcionario import Funcionario
from entidades.cargo import Cargo
from telas.tela_recursos_humanos import TelaRh

class ControladorRh:
    def __init__(self):
        #self.__rh = rh
        self.__tela = TelaRh()
        #self.__controlador_sistema = controlador_sistema

    def incluir_funcionario(self):
        dados = self.__tela.pega_dados_funcionario()
        cargo = Cargo(dados["tipo_cargo"])
        funcionario = Funcionario(
            cpf=dados["cpf"],
            nome=dados["nome"],
            idade=dados["idade"],
            telefone=dados["telefone"],
            email=dados["email"],
            cargo=cargo
        )
        self.__rh.adicionar_funcionario(funcionario)

    def alterar_funcionario(self):
        cpf = self.__tela.seleciona_funcionario()
        novos_dados = self.__tela.pega_dados_funcionario()
        self.__rh.alterar_funcionario(cpf, novos_dados)

    def excluir_funcionario(self):
        cpf = self.__tela.seleciona_funcionario()
        self.__rh.excluir_funcionario(cpf)

    def listar_funcionarios(self):
        lista = self.__rh.listar_funcionarios()
        self.__tela.mostra_lista(lista)

    def realizar_pagamento(self):
        cpf = self.__tela.seleciona_funcionario()
        metodo = self.__tela.pega_metodo_pagamento()
        resultado = self.__rh.realizar_pagamento(cpf, metodo)
        self.__tela.mostra_mensagem(resultado)

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes = {
            1: self.incluir_funcionario,
            2: self.alterar_funcionario,
            3: self.excluir_funcionario,
            4: self.listar_funcionarios,
            5: self.realizar_pagamento,
            0: self.retornar
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
            else:
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")
