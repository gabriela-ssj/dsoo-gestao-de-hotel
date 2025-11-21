from entidades.hospede import Hospede
from entidades.quarto import Quarto
from entidades.servico_de_quarto import ServicoDeQuarto
from entidades.pet import Pet
from typing import List, Optional

from datetime import datetime, date, timedelta


class Reserva:
    _next_id = 1

    def __init__(
            self,
            hospedes: List[Hospede],
            quartos: List[Quarto],
            data_checkin: date,
            data_checkout: date,
            status: str = "pendente",
            pets: Optional[List[Pet]] = None
    ):
        if not all(isinstance(h, Hospede) for h in hospedes):
            raise TypeError("A lista de hóspedes deve conter apenas objetos Hospede.")
        if not all(isinstance(q, Quarto) for q in quartos):
            raise TypeError("A lista de quartos deve conter apenas objetos Quarto.")

        self.__id = Reserva._next_id
        Reserva._next_id += 1

        self.__hospedes = hospedes
        self.__quartos = quartos

        self.__data_checkin = data_checkin
        self.__data_checkout = data_checkout
        
        if self.__data_checkin >= self.__data_checkout:
            raise ValueError("Data de check-out deve ser posterior à data de check-in.")

        self.__status = status
        self.__valor_total = 0.0
        self.__servicos_quarto: List[ServicoDeQuarto] = []
        self.__pets: List[Pet] = pets if pets is not None else []

    @property
    def id(self) -> int:
        return self.__id

    @property
    def hospedes(self) -> List[Hospede]:
        return self.__hospedes

    @property
    def quartos(self) -> List[Quarto]:
        return self.__quartos

    @property
    def data_checkin(self) -> date:
        return self.__data_checkin

    @property
    def data_checkout(self) -> date:
        return self.__data_checkout

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, novo_status: str):
        valid_status = ["pendente", "confirmada", "cancelada", "check-in", "check-out", "paga"]
        if novo_status not in valid_status:
            raise ValueError(f"Status inválido: {novo_status}. Use um dos seguintes: {', '.join(valid_status)}")
        self.__status = novo_status

    @property
    def valor_total(self) -> float:
        self.calcular_valor_total() 
        return self.__valor_total

    @property
    def servicos_quarto(self) -> List[ServicoDeQuarto]:
        return self.__servicos_quarto

    @property
    def pets(self) -> List[Pet]:
        return self.__pets

    def adicionar_servico_quarto(self, servico: ServicoDeQuarto):
        if not isinstance(servico, ServicoDeQuarto):
            raise TypeError("O objeto adicionado deve ser uma instância de ServicoDeQuarto.")
        self.__servicos_quarto.append(servico)
        self.calcular_valor_total()

    def adicionar_pet(self, pet: Pet):
        if not isinstance(pet, Pet):
            raise TypeError("O objeto adicionado deve ser uma instância de Pet.")
        self.__pets.append(pet)
        self.calcular_valor_total()

    def remover_pet(self, pet: Pet):
        if pet in self.__pets:
            self.__pets.remove(pet)
            self.calcular_valor_total()
            return True
        return False

    def reservar_quartos(self):
        for quarto in self.__quartos:
            if not quarto.reservar_quarto():
                print(f"Não foi possível reservar o quarto {quarto.numero}. Ele pode já estar ocupado.")
            quarto.alocar_hospedes(self.__hospedes) 
            for pet in self.__pets:
                quarto.adicionar_pet(pet)
        self.calcular_valor_total()

    def liberar_quartos(self):
        for quarto in self.__quartos:
            quarto.liberar_quarto()
        self.calcular_valor_total()

    def editar_reserva(self, nova_data_checkin: Optional[date] = None, nova_data_checkout: Optional[date] = None,
                         novos_quartos: Optional[List[Quarto]] = None, novos_hospedes: Optional[List[Hospede]] = None,
                         novos_pets: Optional[List[Pet]] = None):
        
        if nova_data_checkin:
            if not isinstance(nova_data_checkin, date):
                raise TypeError("Nova data de check-in deve ser um objeto date.")
            if nova_data_checkin >= self.__data_checkout:
                raise ValueError("Nova data de check-in deve ser anterior à data de check-out.")
            self.__data_checkin = nova_data_checkin

        if nova_data_checkout:
            if not isinstance(nova_data_checkout, date):
                raise TypeError("Nova data de check-out deve ser um objeto date.")
            if nova_data_checkout <= self.__data_checkin:
                raise ValueError("Nova data de check-out deve ser posterior à data de check-in.")
            self.__data_checkout = nova_data_checkout

        if novos_quartos is not None:
            self.liberar_quartos()
            self.__quartos = novos_quartos
            self.reservar_quartos()

        if novos_hospedes is not None:
            if not all(isinstance(h, Hospede) for h in novos_hospedes):
                raise TypeError("A lista de novos hóspedes deve conter apenas objetos Hospede.")
            self.__hospedes = novos_hospedes
            for quarto in self.__quartos:
                quarto.alocar_hospedes(self.__hospedes)
            self.calcular_valor_total()

        if novos_pets is not None:
            if not all(isinstance(p, Pet) for p in novos_pets):
                raise TypeError("A lista de novos pets deve conter apenas objetos Pet.")
            self.__pets = novos_pets
            for quarto in self.__quartos:
                for pet in self.__pets:
                    quarto.adicionar_pet(pet)
            self.calcular_valor_total()

        self.calcular_valor_total()

    def calcular_valor_diarias_e_pets(self) -> float:
        """ Calcula o valor base da hospedagem (diárias + taxa pet), excluindo serviços de quarto. """
        dias = self._calcular_dias()
        total_diarias_e_pets = 0.0

        for quarto in self.__quartos:
            num_adultos_reserva = sum(1 for hospede in self.__hospedes if hospede.is_adulto())
            if num_adultos_reserva > 0: 
                total_diarias_e_pets += quarto.valor_diaria * dias

        total_diarias_e_pets += sum(pet.calcular_taxa_pet(50.0) for pet in self.__pets)
        
        return total_diarias_e_pets

    def get_valor_servicos_adicionais(self) -> float:
        """ Retorna apenas o valor total acumulado dos serviços de quarto. """
        return sum(s.valor for s in self.__servicos_quarto if s.valor is not None)

    def calcular_valor_total(self):
        dias = self._calcular_dias()
        total = 0.0

        for quarto in self.__quartos:
            num_adultos_reserva = sum(1 for hospede in self.__hospedes if hospede.is_adulto())
            if num_adultos_reserva > 0: 
                total += quarto.valor_diaria * dias

        total += sum(s.valor for s in self.__servicos_quarto if s.valor is not None)
        total += sum(pet.calcular_taxa_pet(50.0) for pet in self.__pets)
        self.__valor_total = total

    def _calcular_dias(self) -> int:
        return (self.__data_checkout - self.__data_checkin).days

    def __str__(self):
        hospedes_nomes = ", ".join([h.nome for h in self.__hospedes])
        quartos_numeros = ", ".join([str(q.numero) for q in self.__quartos])
        checkin_str = self.__data_checkin.strftime("%d/%m/%Y")
        checkout_str = self.__data_checkout.strftime("%d/%m/%Y")
        return (f"Reserva ID: {self.__id} | Hóspedes: {hospedes_nomes} | Quartos: {quartos_numeros} | "
                f"Check-in: {checkin_str} | Check-out: {checkout_str} | Status: {self.__status} | "
                f"Valor Total: R$ {self.valor_total:.2f}")
    
    def get_all_data(self) -> dict:
        hospedes_data = []
        quartos_data = []
        servicos_data = []
        pets_data = []

        for hospede in self.__hospedes:
            hospedes_data.append({
                "nome": hospede.nome,
                "cpf": hospede.cpf,
                "idade": hospede.idade,
                "telefone": hospede.telefone,
                "email": hospede.email
            })

        for quarto in self.__quartos:
            quarto_info = {
                "numero": quarto.numero,
                "tipo": type(quarto).__name__,
                "valor_diaria": quarto.valor_diaria,
                "disponibilidade": quarto.disponibilidade,
                "capacidade_pessoas": quarto.capacidade_pessoas
            }
            if hasattr(quarto, 'hidro'):
                quarto_info["hidro"] = quarto.hidro
            quartos_data.append(quarto_info)

        for servico in self.__servicos_quarto:
            servicos_data.append({
                "tipo_servico": servico.tipo_servico,
                "valor": servico.valor,
                "status": servico.status,
                "quarto_numero": servico.quarto.numero if servico.quarto else None, 
                "funcionario_nome": servico.funcionario.nome if servico.funcionario else None,
                "funcionario_cpf": servico.funcionario.cpf if servico.funcionario else None
            })

        for pet in self.__pets:
            pets_data.append({
                "nome_pet": pet.nome_pet,
                "especie": pet.especie
            })

        return {
            "id": self.__id,
            "hospedes": hospedes_data,
            "quartos": quartos_data,
            "checkin": self.__data_checkin.strftime("%d/%m/%Y"),
            "checkout": self.__data_checkout.strftime("%d/%m/%Y"),
            "status": self.__status,
            "valor_total": round(self.valor_total, 2),
            "servicos_quarto": servicos_data,
            "pets": pets_data,
            "dias_reservados": self._calcular_dias()
        }