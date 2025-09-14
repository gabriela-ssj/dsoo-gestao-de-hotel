from hospede import Hospede
from funcionario import Funcionario
from quarto import Quarto
from reserva import Reserva
from recursos_humanos import Rh
from typing import List

class Hotel:
    def __init__(
        self,
        nome: str,
        hospedes: List[Hospede] = None,
        funcionarios: List[Funcionario] = None,
        quartos: List[Quarto] = None,
        reservas: List[Reserva] = None,
        recursos_humanos: Rh = None
    ):
        if not isinstance(nome, str):
            raise TypeError("O nome do hotel deve ser uma string")

        self.__nome = nome
        self.__hospedes = hospedes if hospedes is not None else []
        self.__funcionarios = funcionarios if funcionarios is not None else []
        self.__quartos = quartos if quartos is not None else []
        self.__reservas = reservas if reservas is not None else []
        self.__recursos_humanos = recursos_humanos

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if not isinstance(nome, str):
            raise TypeError("O nome do hotel deve ser uma string")
        self.__nome = nome

    @property
    def recursos_humanos(self):
        return self.__recursos_humanos

    def adicionar_hospede(self, hospede: Hospede):
        self.__hospedes.append(hospede)

    def excluir_hospede(self, cpf: str):
        self.__hospedes = [h for h in self.__hospedes if h.cpf != cpf]

    def listar_hospedes(self) -> List[str]:
        return [f"{h.nome} - CPF: {h.cpf}" for h in self.__hospedes]

    def adicionar_funcionario(self, funcionario: Funcionario):
        self.__funcionarios.append(funcionario)

    def adicionar_quarto(self, quarto: Quarto):
        self.__quartos.append(quarto)

    def excluir_quarto(self, numero: int):
        self.__quartos = [q for q in self.__quartos if q.numero != numero]

    def alterar_quarto(self, numero: int, novos_dados: dict):
        for quarto in self.__quartos:
            if quarto.numero == numero:
                for chave, valor in novos_dados.items():
                    if hasattr(quarto, chave):
                        setattr(quarto, chave, valor)

    def listar_quartos(self) -> List[str]:
        return [
            f"Quarto {q.numero} - Diária: R$ {q.valor_diaria:.2f} - Disponível: {q.disponibilidade}"
            for q in self.__quartos
        ]

    def adicionar_reserva(self, reserva: Reserva):
        self.__reservas.append(reserva)

    def listar_reservas(self) -> List[str]:
        return [
            f"Reserva de {len(r.hospedes)} hóspede(s) - Check-in: {r.data_checkin} - Status: {r.status}"
            for r in self.__reservas
        ]
