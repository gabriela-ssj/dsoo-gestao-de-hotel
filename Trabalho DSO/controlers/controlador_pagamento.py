from entidades.pagamento import Pagamento
from telas.tela_pagamento import TelaPagamento
from controlers.controlador_reserva import ControladorReserva
from entidades.reserva import Reserva

from typing import List, Optional

class ControladorPagamento:
    def __init__(self, controlador_reserva: ControladorReserva):
        self.__pagamentos: list[Pagamento] = []
        self.__tela = TelaPagamento()
        self.__controlador_reserva = controlador_reserva

    def abre_tela(self):
        opcoes = {
            1: self.realizar_pagamento,
            2: self.alterar_metodo_pagamento,
            3: self.exibir_comprovante,
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

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando...")

    def _buscar_pagamento_por_reserva(self, reserva_id: int) -> Optional[Pagamento]:
        for pagamento in self.__pagamentos:
            if pagamento.reserva.id == reserva_id:
                return pagamento
        return None

    def realizar_pagamento(self):
        reserva_id = self.__tela.seleciona_reserva_para_pagamento()
        if not reserva_id:
            return

        reserva: Optional[Reserva] = self.__controlador_reserva.selecionar_reserva(reserva_id)
        if not reserva:
            self.__tela.mostra_mensagem(f"Reserva com ID {reserva_id} não encontrada.")
            return

        pagamento_existente = self._buscar_pagamento_por_reserva(reserva_id)

        if pagamento_existente and pagamento_existente.status == "confirmado":
            self.__tela.mostra_mensagem(f"Pagamento para Reserva ID {reserva_id} já está confirmado.")
            return

        if not pagamento_existente:
            metodo = self.__tela.pega_metodo_pagamento()
            if not metodo:
                self.__tela.mostra_mensagem("Operação cancelada.")
                return
            try:
                novo_pagamento = Pagamento(reserva, metodo)
                self.__pagamentos.append(novo_pagamento)
                pagamento_existente = novo_pagamento
                self.__tela.mostra_mensagem(f"Novo registro de pagamento criado para Reserva ID {reserva_id}.")
            except (TypeError, ValueError) as e:
                self.__tela.mostra_mensagem(f"Erro ao criar pagamento: {e}")
                return

        if pagamento_existente.status == "pendente":
            valor_a_pagar = self.__tela.pega_valor_pagamento()
            if valor_a_pagar is None:
                self.__tela.mostra_mensagem("Valor inválido. Operação cancelada.")
                return

            try:
                pagamento_confirmado = pagamento_existente.pagar(valor_a_pagar)
                self.__tela.mostra_mensagem(
                    f"Valor de R\$ {valor_a_pagar:.2f} recebido para Reserva ID {reserva_id}.")

                if pagamento_confirmado:
                    reserva.status = "paga"
                    self.__tela.mostra_mensagem(
                        f"Pagamento para Reserva ID {reserva_id} confirmado! Status da reserva atualizado para 'paga'.")
                else:
                    self.__tela.mostra_mensagem(
                        f"Pagamento parcial para Reserva ID {reserva_id}. Restante a pagar: R\$ {max(0, pagamento_existente.valor_total_reserva - pagamento_existente.valor_pago):.2f}")
            except ValueError as e:
                self.__tela.mostra_mensagem(f"Erro ao processar pagamento: {e}")
            except Exception as e:
                self.__tela.mostra_mensagem(f"Erro inesperado ao realizar pagamento: {e}")
        else:
            self.__tela.mostra_mensagem(
                f"Pagamento para Reserva ID {reserva_id} já está em status '{pagamento_existente.status}'.")

    def alterar_metodo_pagamento(self):
        reserva_id = self.__tela.seleciona_reserva_para_pagamento()
        if not reserva_id:
            return

        pagamento_alvo = self._buscar_pagamento_por_reserva(reserva_id)
        if not pagamento_alvo:
            self.__tela.mostra_mensagem(f"Nenhum registro de pagamento encontrado para Reserva ID {reserva_id}.")
            return

        if pagamento_alvo.status == "confirmado":
            self.__tela.mostra_mensagem(
                "Não é possível alterar o método de pagamento de um pagamento já confirmado.")
            return

        novo_metodo = self.__tela.pega_metodo_pagamento()
        if not novo_metodo:
            self.__tela.mostra_mensagem("Operação cancelada.")
            return

        try:
            pagamento_alvo.metodo_pagamento = novo_metodo
            self.__tela.mostra_mensagem(
                f"Método de pagamento da Reserva ID {reserva_id} alterado para '{novo_metodo}'.")
        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro ao alterar método de pagamento: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado: {e}")

    def exibir_comprovante(self):
        reserva_id = self.__tela.seleciona_reserva_para_pagamento()
        if not reserva_id:
            return

        pagamento_alvo = self._buscar_pagamento_por_reserva(reserva_id)
        if not pagamento_alvo:
            self.__tela.mostra_mensagem(f"Nenhum registro de pagamento encontrado para Reserva ID {reserva_id}.")
            return

        comprovante = pagamento_alvo.gerar_comprovante()
        self.__tela.mostra_comprovante(comprovante)
