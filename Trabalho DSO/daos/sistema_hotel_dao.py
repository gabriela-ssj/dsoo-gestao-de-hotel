from daos.dao import DAO
from entidades.hotel import Hotel


class SistemaHotelDAO(DAO):
    def __init__(self):
        super().__init__('sistema_hotel.pkl')

    def add(self, hotel: Hotel):
        if hotel is not None and isinstance(hotel, Hotel):
            nome = hotel.nome.lower().strip()
            super().add(nome, hotel)

    def update(self, hotel: Hotel):
        if hotel is not None and isinstance(hotel, Hotel):
            nome = hotel.nome.lower().strip()
            super().update(nome, hotel)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key.lower().strip())

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key.lower().strip())
