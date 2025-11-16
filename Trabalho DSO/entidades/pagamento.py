from entidades.reserva import Reserva
from datetime import datetime
from typing import Optional


class Pagamento:
    _next_id = 1

    def __init__(self, reserva: Reserva, metodo_pagamento: str):
        if not isinstance(reserva, Reserva):
            raise TypeError("Pagamento deve estar associado a um objeto Reserva.")
        if not isinstance(metodo_pagamento, str) or not metodo_pagamento.strip():
            raise ValueError("Método de pagamento inválido.")

        self.__id = Pagamento._next_id
        Pagamento._next_id += 1

        self.__reserva = reserva
        self.__metodo_pagamento = metodo_pagamento
        self.__valor_total_reserva = reserva.valor_total
        self.__valor_pago = 0.0
        self.__status = "pendente"
        self.__data_pagamento: Optional[datetime] = None

    @property
    def id(self) -> int:
        return self.__id

    @property
    def reserva(self) -> Reserva:
        return self.__reserva

    @property
    def metodo_pagamento(self) -> str:
        return self.__metodo_pagamento

    @metodo_pagamento.setter
    def metodo_pagamento(self, metodo: str):
        if not isinstance(metodo, str) or not metodo.strip():
            raise ValueError("Método de pagamento inválido.")
        self.__metodo_pagamento = metodo

    @property
    def status(self) -> str:
        return self.__status

    @property
    def valor_total_reserva(self) -> float:
        return self.__valor_total_reserva

    @property
    def valor_pago(self) -> float:
        return self.__valor_pago

    @property
    def data_pagamento(self) -> Optional[datetime]:
        return self.__data_pagamento

    def pagar(self, valor: float) -> bool:
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("Valor a ser pago deve ser um número positivo.")
        if self.__status == "confirmado":
            raise ValueError("Este pagamento já foi confirmado.")

        self.__valor_pago += valor
        return self._verificar_status_pagamento()

    def _verificar_status_pagamento(self) -> bool:
        if self.__valor_pago >= self.__valor_total_reserva and self.__status != "confirmado":
            self.__status = "confirmado"
            self.__data_pagamento = datetime.now()
            return True
        elif self.__valor_pago < self.__valor_total_reserva:
            self.__status = "pendente"
            return False
        return False

    def gerar_comprovante(self) -> dict:
        self.reserva.calcular_valor_total()

        valor_atual_reserva = self.reserva.valor_total

        return {
            "ID do Pagamento": self.__id,
            "ID da Reserva": self.__reserva.id,
            "Hóspede Principal": self.__reserva.hospedes[0].nome if self.__reserva.hospedes else "N/A",
            "Valor Total da Reserva (Atual)": f"R$ {valor_atual_reserva:.2f}",
            "Valor Calculado no Pagamento": f"R$ {self.__valor_total_reserva:.2f}",
            # Valor no momento da criação do Pagamento
            "Valor Pago": f"R$ {self.__valor_pago:.2f}",
            "Restante a Pagar": f"R$ {max(0, self.__valor_total_reserva - self.__valor_pago):.2f}",
            "Método de Pagamento": self.__metodo_pagamento,
            "Status do Pagamento": self.__status,
            "Data do Pagamento": self.__data_pagamento.strftime(
                "%d/%m/%Y %H:%M:%S") if self.__data_pagamento else "Não pago"
        }

    def __str__(self):
        checkin_str = self.__reserva.data_checkin.strftime("%d/%m/%Y")
        checkout_str = self.__reserva.data_checkout.strftime("%d/%m/%Y")
        return (f"Pagamento ID: {self.__id} | Reserva ID: {self.__reserva.id} | "
                f"Check-in: {checkin_str} | Check-out: {checkout_str} | "
                f"Valor Total: R$ {self.__valor_total_reserva:.2f} | Valor Pago: R$ {self.__valor_pago:.2f} | "
                f"Status: {self.__status} | Método: {self.__metodo_pagamento}")
