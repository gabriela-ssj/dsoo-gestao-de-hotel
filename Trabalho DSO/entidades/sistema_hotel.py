from entidades.hotel import Hotel
from typing import List, Optional

class SistemaHotel:
    def __init__(self):
        self.__hoteis: List[Hotel] = []

    @property
    def hoteis(self) -> List[Hotel]:
        return self.__hoteis.copy()

    def incluir_hotel(self, novo_hotel: Hotel) -> bool:
        if any(h.nome == novo_hotel.nome for h in self.__hoteis):
            return False  
        self.__hoteis.append(novo_hotel)
        return True

    def excluir_hotel(self, nome: str) -> bool:
        hotel = self.buscar_hotel(nome)
        if hotel:
            self.__hoteis.remove(hotel)
            return True
        return False

    def alterar_hotel(self, nome: str, novos_dados: dict) -> bool:
        hotel = self.buscar_hotel(nome)
        if hotel:
            for chave, valor in novos_dados.items():
                if hasattr(hotel, chave):
                    setattr(hotel, chave, valor)
            return True
        return False

    def listar_hoteis(self) -> List[str]:
        return [
            f"{h.nome} - {len(h.quartos)} quarto(s) - {len(h.hospedes)} hóspede(s)"
            for h in self.__hoteis
        ]

    def buscar_hotel(self, nome: str) -> Optional[Hotel]:
        return next((h for h in self.__hoteis if h.nome.lower() == nome.lower()), None)
