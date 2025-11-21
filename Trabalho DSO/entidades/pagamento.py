from entidades.reserva import Reserva
from datetime import datetime
import uuid
from typing import Optional, Dict, Any

class Pagamento:
    def __init__(self, reserva: Reserva, metodo_pagamento: str):
        self.__id = uuid.uuid4().int % 1000  
        self.__reserva = reserva
        self.__metodo_pagamento = metodo_pagamento
        self.__valor_pago = 0.0
        self.__status = "pendente"
        self.__data_pagamento: Optional[datetime] = None
        self.__valor_total_reserva = 0.0
        
        self.atualizar_valor_total()
        
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
    def metodo_pagamento(self, novo_metodo: str):
        metodos_validos = ["Debito", "Credito", "Dinheiro", "Pix"]
        if novo_metodo not in metodos_validos:
            raise ValueError(f"Método de pagamento '{novo_metodo}' inválido. Use um de: {', '.join(metodos_validos)}.")
        self.__metodo_pagamento = novo_metodo

    @property
    def valor_pago(self) -> float:
        return self.__valor_pago

    @property
    def status(self) -> str:
        return self.__status

    @property
    def valor_total_reserva(self) -> float:
        return self.__valor_total_reserva

    def atualizar_valor_total(self):
        """ 
        Recalcula e atualiza o valor total da reserva no objeto Pagamento, 
        buscando o valor mais recente da Reserva (que inclui serviços).
        """
        try:
            self.__valor_total_reserva = self.__reserva.valor_total
        except Exception as e:
            raise ValueError(f"Erro ao obter o valor total da reserva para o pagamento: {e}")

    def pagar(self, valor: float) -> bool:
        """ Processa o pagamento e retorna True se o valor total foi atingido. """
        if valor <= 0:
            raise ValueError("O valor do pagamento deve ser maior que zero.")
        
        self.atualizar_valor_total() 
        
        valor_restante = self.__valor_total_reserva - self.__valor_pago
        
        if valor > valor_restante:
            raise ValueError(f"Valor pago (R$ {valor:.2f}) excede o restante devido (R$ {valor_restante:.2f}).")

        self.__valor_pago += valor
        
        if self.__valor_pago >= self.__valor_total_reserva:
            self.__status = "confirmado"
            self.__data_pagamento = datetime.now()
            return True
        
        return False

    def gerar_comprovante(self) -> Dict[str, Any]:
        """ 
        Gera um dicionário (Dict) com os dados do comprovante, 
        no formato esperado pela TelaPagamento.
        """
        self.atualizar_valor_total()

        valor_devido = self.valor_total_reserva
        restante = max(0.0, valor_devido - self.__valor_pago)

        hospede_principal = "N/A"
        if self.reserva.hospedes:
            try:
                hospede_principal = self.reserva.hospedes[0].nome
            except Exception:
                hospede_principal = "Erro ao obter nome do hóspede"

        quartos_info = [f"{q.numero} ({type(q).__name__}, R$ {q.valor_diaria:.2f})" for q in self.reserva.quartos]
        servicos_info = [f"{s.tipo_servico}: R$ {s.valor:.2f}" for s in self.reserva.servicos_quarto if s.valor is not None]

        return {
            "ID do Pagamento": self.__id,
            "ID da Reserva": self.reserva.id,
            "Hóspede Principal": hospede_principal,
            "Quartos": quartos_info,
            "Status da Reserva": self.reserva.status,
            "Valor Total da Reserva": self.reserva.valor_total,
            "Valor Pago": self.__valor_pago,
            "Restante a Pagar": restante,
            "Método de Pagamento": self.__metodo_pagamento,
            "Status do Pagamento": self.__status,
            "Data do Pagamento": self.__data_pagamento.strftime("%d/%m/%Y %H:%M:%S") if self.__data_pagamento else "Pagamento pendente",
            "Serviços Adicionais": servicos_info
        }