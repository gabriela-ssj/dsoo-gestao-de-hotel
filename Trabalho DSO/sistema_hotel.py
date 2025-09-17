from hotel import Hotel
from typing import List

class SistemaHotel:
    def __init__(self):
        self.__hoteis: List[Hotel] = []

    def incluir_hotel(self, hotel: Hotel):
        self.__hoteis.append(hotel)

    def excluir_hotel(self, nome: str):
        self.__hoteis = [h for h in self.__hoteis if h.nome != nome]

    def alterar_hotel(self, nome: str, novos_dados: dict):
        for hotel in self.__hoteis:
            if hotel.nome == nome:
                for chave, valor in novos_dados.items():
                    if hasattr(hotel, chave):
                        setattr(hotel, chave, valor)

    def listar_hoteis(self) -> List[str]:
        return [f"{h.nome} - {len(h.quartos)} quartos - {len(h.hospedes)} hóspedes" for h in self.__hoteis]

    def buscar_hotel(self, nome: str) -> Hotel:
        for hotel in self.__hoteis:
            if hotel.nome == nome:
                return hotel
        return None
