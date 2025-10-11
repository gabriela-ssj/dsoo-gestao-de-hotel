from entidades.reserva import Reserva

class Pagamento:
    def __init__(self, reserva: Reserva, metodo_pagamento: str, status: str = "pendente"):
        self.__reserva = reserva
        self.__metodo_pagamento = metodo_pagamento
        self.__status = status
        self.__valor_calculado = self.__calcular_valor_total()
        self.__valor_pago = 0.0

    @property
    def reserva(self):
        return self.__reserva

    @property
    def metodo_pagamento(self):
        return self.__metodo_pagamento

    @metodo_pagamento.setter
    def metodo_pagamento(self, metodo: str):
        self.__metodo_pagamento = metodo

    @property
    def status(self):
        return self.__status

    @property
    def valor_calculado(self):
        return self.__valor_calculado

    @property
    def valor_pago(self):
        return self.__valor_pago

    def pagar(self, valor: float):
        if valor <= 0:
            raise ValueError("O valor do pagamento deve ser positivo.")
        self.__valor_pago += valor
        self.__validar_pagamento()

    def cancelar_pagamento(self):
        if self.__status != "confirmado":
            raise ValueError("Não é possível cancelar um pagamento que ainda está pendente.")
        self.__valor_pago = 0.0
        self.__status = "cancelado"
        self.__reserva.status = "cancelada"

    def __validar_pagamento(self):
        if self.__valor_pago >= self.__valor_calculado:
            self.__status = "confirmado"
            self.__reserva.status = "paga"
        else:
            self.__status = "pendente"

    def __calcular_valor_total(self) -> float:
        dias = self.__reserva._Reserva__calcular_dias()
        total = 0.0

        for quarto in self.__reserva.quartos:
            for hospede in self.__reserva.hospedes:
                if hospede.is_adulto():
                    total += quarto.valor_diaria * dias

        total += sum(servico.valor for servico in self.__reserva.servicos_quarto)
        total += sum(pet.calcular_taxa_pet(50.0) for pet in self.__reserva.pets)

        return total

    def gerar_comprovante(self) -> dict:
        return {
            "quartos": [q.numero for q in self.__reserva.quartos],
            "metodo": self.__metodo_pagamento,
            "valor_calculado": self.__valor_calculado,
            "valor_pago": self.__valor_pago,
            "status": self.__status,
            "pets": [str(pet) for pet in self.__reserva.pets]
        }
