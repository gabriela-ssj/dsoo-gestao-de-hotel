from hospede import Hospede
from quarto import Quarto
from reserva import Reserva
from typing import List
from recursos_humanos import Rh  


class Hotel:
    def __init__(
        self,
        nome: str,
        hospedes: List[Hospede] = None,
        quartos: List[Quarto] = None,
        reservas: List[Reserva] = None,
        recursos_humanos: Rh = None
    ):
        if not isinstance(nome, str):
            raise TypeError("O nome do hotel deve ser uma string")

        self.__nome = nome
        self.__hospedes = hospedes if hospedes is not None else []
        self.__quartos = quartos if quartos is not None else []
        self.__reservas = reservas if reservas is not None else []
        self.recursos_humanos = recursos_humanos or Rh()

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("O nome do hotel deve ser uma string")
        self.__nome = nome

    @property
    def quartos(self):
        return self.__quartos

    @property
    def hospedes(self):
        return self.__hospedes
    
    def adicionar_hospede(self, hospede: Hospede):
        duplicado = False
        for h in self.__hospedes:
            if h.cpf == hospede.cpf:
                print(f"⚠️ Hóspede com CPF {hospede.cpf} já está cadastrado.")
                duplicado = True
        if not duplicado:
            self.__hospedes.append(hospede)
            print("✅ Hóspede adicionado com sucesso.")

    def excluir_hospede(self, cpf: str):
        for h in self.__hospedes:
            if h.cpf == cpf:
                self.__hospedes.remove(h)
                print(f"✅ Hóspede com CPF {cpf} excluído.")
                return
        print(f"⚠️ Hóspede com CPF {cpf} não encontrado.")

    def listar_hospedes(self) -> List[str]:
        return [f"{h.nome} - CPF: {h.cpf}" for h in self.__hospedes]

    def adicionar_quarto(self, quarto: Quarto):
        duplicado = False
        for q in self.__quartos:
            if q.numero == quarto.numero:
                print(f"⚠️ Quarto número {quarto.numero} já está cadastrado.")
                duplicado = True
        if not duplicado:
            self.__quartos.append(quarto)
            print("✅ Quarto adicionado com sucesso.")

    def excluir_quarto(self, numero: int):
        for q in self.__quartos:
            if q.numero == numero:
                self.__quartos.remove(q)
                print(f"✅ Quarto número {numero} excluído.")
                return
        print(f"⚠️ Quarto número {numero} não encontrado.")

    def alterar_quarto(self, numero: int, novos_dados: dict):
        for quarto in self.__quartos:
            if quarto.numero == numero:
                for chave, valor in novos_dados.items():
                    if hasattr(quarto, chave):
                        setattr(quarto, chave, valor)
                print(f"✅ Quarto número {numero} alterado.")
                return
        print(f"⚠️ Quarto número {numero} não encontrado.")

    def listar_quartos(self) -> List[str]:
        return [
            f"Quarto {q.numero} - Diária: R$ {q.valor_diaria:.2f} - Disponível: {q.disponibilidade}"
            for q in self.__quartos
        ]

    def adicionar_reserva(self, nova_reserva: Reserva):
        duplicado = False
        for reserva in self.__reservas:
            for hospede_novo in nova_reserva.hospedes:
                for hospede_existente in reserva.hospedes:
                    if (
                        hospede_novo.cpf == hospede_existente.cpf
                        and reserva.data_checkin == nova_reserva.data_checkin
                    ):
                        print(f"⚠️ Hóspede {hospede_novo.nome} já possui reserva para {nova_reserva.data_checkin}.")
                        duplicado = True
        if not duplicado:
            self.__reservas.append(nova_reserva)
            print("✅ Reserva adicionada com sucesso.")

    def listar_reservas(self) -> List[str]:
        return [
            f"Reserva de {len(r.hospedes)} hóspede(s) - Check-in: {r.data_checkin} - Status: {r.status}"
            for r in self.__reservas
        ]
