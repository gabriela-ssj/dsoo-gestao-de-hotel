from entidades.pagamento import Pagamento
from telas.tela_pagamento import TelaPagamento

class ControladorPagamento:
    def __init__(self):
        self.__tela = TelaPagamento()
        self.tela_aberta = True

    def realizar_pagamento(self):
        valor = self.__tela.pega_valor_pagamento()
        try:
            self.__pagamento.pagar(valor)
            self.__tela.mostra_mensagem("✅ Pagamento realizado.")
        except ValueError as e:
            self.__tela.mostra_mensagem(f"⚠️ Erro: {str(e)}")

    def alterar_metodo_pagamento(self):
        novo_metodo = self.__tela.pega_metodo_pagamento()
        self.__pagamento.metodo_pagamento = novo_metodo
        self.__tela.mostra_mensagem("✅ Método de pagamento alterado.")

    def exibir_comprovante(self):
        comprovante = self.__pagamento.comprovante_pagamento()
        self.__tela.mostra_mensagem(comprovante)

    def retornar(self):
        self.tela_aberta = False

    def abre_tela(self):
        self.tela_aberta = True
        opcoes = {
            1: self.realizar_pagamento,
            2: self.alterar_metodo_pagamento,
            3: self.exibir_comprovante,
            0: self.retornar
        }
        while self.tela_aberta:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
            else:
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")
