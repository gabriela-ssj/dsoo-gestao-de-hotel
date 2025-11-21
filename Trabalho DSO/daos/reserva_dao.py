from daos.dao import DAO
from entidades.reserva import Reserva

class ReservaDAO(DAO):
    def __init__(self):
        super().__init__("reservas.pkl")
        self.__ultimo_id = self._descobrir_ultimo_id()

    def _descobrir_ultimo_id(self):
        if not self.get_all():
            return 0
        return max(reserva.id for reserva in self.get_all().values())

    def add(self, reserva: Reserva):
        if reserva is not None and isinstance(reserva, Reserva):
            self.__ultimo_id += 1
            reserva.id = self.__ultimo_id
            super().add(reserva.id, reserva)

    def get(self, key: int):
        return super().get(key)

    def remove(self, key: int):
        return super().remove(key)

    def get_all(self):
        return super().get_all()
