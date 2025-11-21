from entidades.pagamento import Pagamento
from telas.tela_pagamento import TelaPagamento
from controlers.controlador_reserva import ControladorReserva
from entidades.reserva import Reserva
from daos.pagamento_dao import PagamentoDAO
from typing import Optional

class ControladorPagamento:
    def __init__(self, controlador_reserva: ControladorReserva):
        self.__tela = TelaPagamento()
        self.__controlador_reserva = controlador_reserva
        self.__pagamento_dao = PagamentoDAO()

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
        return self.__pagamento_dao.get(reserva_id)

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
            self.__tela.mostra_mensagem("Pagamento já confirmado.")
            return

        if not pagamento_existente:
            metodo = self.__tela.pega_metodo_pagamento()
            if not metodo:
                self.__tela.mostra_mensagem("Operação cancelada.")
                return

            try:
                pagamento_existente = Pagamento(reserva, metodo)
                self.__pagamento_dao.add(pagamento_existente)
                self.__tela.mostra_mensagem("Pagamento registrado com sucesso.")
            except Exception as e:
                self.__tela.mostra_mensagem(f"Erro ao criar pagamento: {e}")
                return

        try:
            pagamento_existente.atualizar_valor_total()
            self.__pagamento_dao.update(pagamento_existente)
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro ao atualizar valor total: {e}")
            return

        if pagamento_existente.status == "pendente":
            valor_restante = pagamento_existente.valor_total_reserva - pagamento_existente.valor_pago
            valor = self.__tela.pega_valor_pagamento()

            if valor is None:
                self.__tela.mostra_mensagem("Valor inválido.")
                return

            if valor > valor_restante:
                self.__tela.mostra_mensagem(
                    f"Erro: valor excede o restante (R$ {valor_restante:.2f}).")
                return

            try:
                confirmado = pagamento_existente.pagar(valor)
                self.__pagamento_dao.update(pagamento_existente)

                if confirmado:
                    reserva.status = "paga"
                    self.__tela.mostra_mensagem("Pagamento confirmado! Reserva atualizada.")
                else:
                    restante = pagamento_existente.valor_total_reserva - pagamento_existente.valor_pago
                    self.__tela.mostra_mensagem(
                        f"Pagamento parcial. Restante: R$ {restante:.2f}"
                    )
            except Exception as e:
                self.__tela.mostra_mensagem(f"Erro ao processar pagamento: {e}")
        else:
            self.__tela.mostra_mensagem(f"Pagamento já está '{pagamento_existente.status}'.")


    def alterar_metodo_pagamento(self):
        reserva_id = self.__tela.seleciona_reserva_para_pagamento()
        if not reserva_id:
            return

        pagamento = self._buscar_pagamento_por_reserva(reserva_id)
        if not pagamento:
            self.__tela.mostra_mensagem("Pagamento não encontrado.")
            return

        if pagamento.status == "confirmado":
            self.__tela.mostra_mensagem("Não é possível alterar um pagamento confirmado.")
            return

        novo_metodo = self.__tela.pega_metodo_pagamento()

        if not novo_metodo:
            self.__tela.mostra_mensagem("Cancelado.")
            return

        try:
            pagamento.metodo_pagamento = novo_metodo
            self.__pagamento_dao.update(pagamento)
            self.__tela.mostra_mensagem("Método alterado com sucesso.")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")


    def exibir_comprovante(self):
        reserva_id = self.__tela.seleciona_reserva_para_pagamento()
        if not reserva_id:
            return

        pagamento = self._buscar_pagamento_por_reserva(reserva_id)
        if not pagamento:
            self.__tela.mostra_mensagem("Pagamento não encontrado.")
            return

        try:
            pagamento.atualizar_valor_total()
            self.__pagamento_dao.update(pagamento)
            dados = pagamento.gerar_comprovante()
            self.__tela.mostra_comprovante(dados)
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro ao gerar comprovante: {e}")
