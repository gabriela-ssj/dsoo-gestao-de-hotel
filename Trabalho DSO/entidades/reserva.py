from entidades.hospede import Hospede
from entidades.quarto import Quarto
from entidades.servico_de_quarto import ServicoDeQuarto
from entidades.pet import Pet
from typing import List, Optional
from datetime import datetime, timedelta


class Reserva:
    _next_id = 1

    def __init__(
            self,
            hospedes: List[Hospede],
            quartos: List[Quarto],
            data_checkin: str,
            data_checkout: str,
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

        try:
            self.__data_checkin = datetime.strptime(data_checkin, "%d/%m/%Y")
            self.__data_checkout = datetime.strptime(data_checkout, "%d/%m/%Y")
            if self.__data_checkin >= self.__data_checkout:
                raise ValueError("Data de check-out deve ser posterior à data de check-in.")
        except ValueError as e:
            raise ValueError(f"Formato de data inválido (esperado dd/mm/yyyy) ou datas inconsistentes: {e}")

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
    def data_checkin(self) -> datetime:
        return self.__data_checkin

    @property
    def data_checkout(self) -> datetime:
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

    def adicionar_pet(self, pet: Pet):
        if not isinstance(pet, Pet):
            raise TypeError("O objeto adicionado deve ser uma instância de Pet.")
        self.__pets.append(pet)

    def remover_pet(self, pet: Pet):
        if pet in self.__pets:
            self.__pets.remove(pet)
            return True
        return False

    def reservar_quartos(self):
        for quarto in self.__quartos:
            if not quarto.reservar_quarto():
                print(f"⚠️ Não foi possível reservar o quarto {quarto.numero}. Ele pode já estar ocupado.")
            if not quarto.alocar_hospedes(self.__hospedes):
                return False
            for pet in self.__pets:
                quarto.adicionar_pet(pet)

    def liberar_quartos(self):
        for quarto in self.__quartos:
            quarto.liberar_quarto()

    def editar_reserva(self, nova_data_checkin: Optional[str] = None, nova_data_checkout: Optional[str] = None,
                       novos_quartos: Optional[List[Quarto]] = None, novos_hospedes: Optional[List[Hospede]] = None,
                       novos_pets: Optional[List[Pet]] = None):
        if nova_data_checkin:
            try:
                new_checkin = datetime.strptime(nova_data_checkin, "%d/%m/%Y")
                if new_checkin >= self.__data_checkout:
                    raise ValueError("Nova data de check-in deve ser anterior à data de check-out.")
                self.__data_checkin = new_checkin
            except ValueError as e:
                raise ValueError(f"Formato de nova data de check-in inválido: {e}")

        if nova_data_checkout:
            try:
                new_checkout = datetime.strptime(nova_data_checkout, "%d/%m/%Y")
                if new_checkout <= self.__data_checkin:
                    raise ValueError("Nova data de check-out deve ser posterior à data de check-in.")
                self.__data_checkout = new_checkout
            except ValueError as e:
                raise ValueError(f"Formato de nova data de check-out inválido: {e}")

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

        if novos_pets is not None:
            if not all(isinstance(p, Pet) for p in novos_pets):
                raise TypeError("A lista de novos pets deve conter apenas objetos Pet.")
            self.__pets = novos_pets
            for quarto in self.__quartos:
                for pet in self.__pets:
                    quarto.adicionar_pet(pet)

    def calcular_valor_total(self):
        dias = self._calcular_dias()
        total = 0.0

        for quarto in self.__quartos:
            num_adultos_reserva = sum(1 for hospede in self.__hospedes if hospede.is_adulto())
            if num_adultos_reserva > 0:
                total += quarto.valor_diaria * dias

        total += sum(servico.valor for servico in self.__servicos_quarto)
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


        self.calcular_valor_total() # Garante que o valor total está atualizado

        hospedes_data = []
        for hospede in self.__hospedes:
            hospedes_data.append({
                "nome": hospede.nome,
                "cpf": hospede.cpf,
                "idade": hospede.idade,
                "telefone": hospede.telefone,
                "email": hospede.email
            })

        quartos_data = []
        for quarto in self.__quartos:
            quarto_info = {
                "numero": quarto.numero,
                "tipo": type(quarto).__name__,
                "valor_diaria": quarto.valor_diaria,
                "disponibilidade": quarto.disponibilidade,
                "capacidade_pessoas": quarto.capacidade_pessoas
            }
            if hasattr(quarto, 'hidro'): # Adiciona informação de hidro para Suíte
                quarto_info["hidro"] = quarto.hidro
            quartos_data.append(quarto_info)

        servicos_data = []
        for servico in self.__servicos_quarto:
            servicos_data.append({
                "tipo_servico": servico.tipo_servico,
                "valor": servico.valor,
                "status": servico.status,
                "quarto_numero": servico.quarto.numero,
                "funcionario_nome": servico.funcionario.nome,
                "funcionario_cpf": servico.funcionario.cpf
            })

        pets_data = []
        for pet in self.__pets:
            pets_data.append({
                "nome_pet": pet.nome_pet,
                "especie": pet.especie
            })

        return {
            "id": self.__id,
            "hospedes": hospedes_data,
            "quartos": quartos_data,
            "data_checkin": self.__data_checkin.strftime("%d/%m/%Y"),
            "data_checkout": self.__data_checkout.strftime("%d/%m/%Y"),
            "status": self.__status,
            "valor_total": round(self.__valor_total, 2), # Arredonda para 2 casas decimais
            "servicos_de_quarto": servicos_data,
            "pets_na_reserva": pets_data,
            "dias_reservados": self._calcular_dias()
        }