from daos.dao import DAO
from entidades.hotel import Hotel

class HotelDAO(DAO):
    def __init__(self):
        super().__init__('hoteis.pkl')

    def add(self, hotel: Hotel):
        if hotel is not None and isinstance(hotel, Hotel) and isinstance(hotel.nome, str):
            super().add(hotel.nome, hotel)

    def update(self, hotel: Hotel):
        if hotel is not None and isinstance(hotel, Hotel) and isinstance(hotel.nome, str):
            super().update(hotel.nome, hotel)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)
