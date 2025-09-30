from reserva import Reserva

class Pagamento:
    def __init__(self, reserva: Reserva, metodo_pagamento: str, status: str = "pendente"):
        self.__reserva = reserva
        self.__metodo_pagamento = metodo_pagamento
        self.__status = status
        self.__valor_calculado = self.__calcular_valor_total()
        self.__valor_pago = 0.0  

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
            raise ValueError("Valor do pagamento deve ser positivo.")
        self.__valor_pago += valor
        self.__validar_pagamento()

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

        adicionais = 0.0
        if hasattr(self.__reserva, "servicos_quarto"):
            for servico in self.__reserva.servicos_quarto:
                adicionais += servico.valor

        taxa_pet = 0.0
        if hasattr(self.__reserva, "pets"):
            for pet in self.__reserva.pets:
                taxa_pet += pet.calcular_taxa_pet(50.0)  # taxa fixa por animal

        return total + adicionais + taxa_pet

    def comprovante_pagamento(self):
        pets_info = ""
        if hasattr(self.__reserva, "pets") and self.__reserva.pets:
            pets_info = "\n🐾 Pets incluídos:\n" + "\n".join(str(pet) for pet in self.__reserva.pets)
        else:
            pets_info = "\n🐾 Nenhum pet incluído na reserva."

        return (
            f"Comprovante de Pagamento\n"
            f"Reserva: Quarto(s) {[q.numero for q in self.__reserva.quartos]}\n"
            f"Método: {self.__metodo_pagamento}\n"
            f"Valor Calculado: R$ {self.__valor_calculado:.2f}\n"
            f"Valor Pago: R$ {self.__valor_pago:.2f}\n"
            f"Status: {self.__status}"
            f"{pets_info}"
        )
