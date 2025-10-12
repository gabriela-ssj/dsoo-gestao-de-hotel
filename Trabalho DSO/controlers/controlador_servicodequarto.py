from entidades.servico_de_quarto import ServicoDeQuarto
from telas.tela_servicodequarto import TelaServicoDeQuarto

class ControladorServicoDeQuarto:
    def __init__(self, controlador_quarto, controlador_funcionario):
        self.__servicos: list[ServicoDeQuarto] = []
        self.__tela = TelaServicoDeQuarto()
        self.__controlador_quarto = controlador_quarto
        self.__controlador_funcionario = controlador_funcionario

    def abre_tela(self):
        opcoes = {
            1: self.solicitar_servico,
            2: self.listar_servicos,
            3: self.alterar_status_servico,
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
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")

    def solicitar_servico(self):
        dados = self.__tela.pega_dados_servico()
        quarto = self.__controlador_quarto.buscar_quarto(dados["numero_quarto"])
        funcionario = self.__controlador_funcionario.buscar_funcionario_por_nome(dados["nome_funcionario"])

        if not quarto or not funcionario:
            self.__tela.mostra_mensagem("⚠️ Quarto ou funcionário não encontrado.")
            return

        servico = ServicoDeQuarto(quarto, funcionario, dados["tipo_servico"], dados["valor"])
        self.__servicos.append(servico)
        self.__tela.mostra_mensagem(f"✅ Serviço '{servico.tipo_servico}' solicitado para o quarto {quarto.numero}.")

    def listar_servicos(self):
        if not self.__servicos:
            self.__tela.mostra_mensagem("Nenhum serviço registrado.")
            return
        lista = [
            f"{s.tipo_servico} | Quarto: {s.quarto.numero} | Funcionário: {s.funcionario.nome} | Valor: R${s.valor:.2f} | Status: {s.status}"
            for s in self.__servicos
        ]
        self.__tela.mostra_lista(lista)

    def alterar_status_servico(self):
        numero_quarto = self.__tela.seleciona_servico()
        servico = next((s for s in self.__servicos if s.quarto.numero == numero_quarto), None)
        if not servico:
            self.__tela.mostra_mensagem("⚠️ Serviço não encontrado.")
            return

        novo_status = self.__tela.seleciona_status()
        try:
            servico.status = novo_status
            self.__tela.mostra_mensagem(f"✅ Status alterado para '{novo_status}'.")
        except ValueError as e:
            self.__tela.mostra_mensagem(str(e))