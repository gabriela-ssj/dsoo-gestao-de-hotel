from daos.dao import DAO
from entidades.reserva import Reserva


class ReservaDAO(DAO):
    def __init__(self):
        super().__init__("reservas.pkl")
        self.__ultimo_id = self._descobrir_ultimo_id()

    def _descobrir_ultimo_id(self):
        todos = self.get_all()
        if not todos:
            return 0
        return max(reserva.id for reserva in todos)

    def add(self, reserva: Reserva):
        if reserva is not None and isinstance(reserva, Reserva):
            super().add(reserva.id, reserva)

    def get(self, key: int):
        return super().get(key)

    def remove(self, key: int):
        return super().remove(key)

    def get_all(self):
        return super().get_all()
