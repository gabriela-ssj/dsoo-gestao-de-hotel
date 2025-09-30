from hotel import Hotel
from typing import List

class SistemaHotel:
    def __init__(self):
        self.__hoteis: List[Hotel] = []

    @property
    def hoteis(self):
        return self.__hoteis

    def incluir_hotel(self, novo_hotel):
        duplicado = False
        for h in self.__hoteis:
            if h.nome == novo_hotel.nome:
                print(f"⚠️ Hotel '{novo_hotel.nome}' já está cadastrado.")
                duplicado = True
                break
        if not duplicado:
           self.__hoteis.append(novo_hotel)
           print(f"✅ Hotel '{novo_hotel.nome}' incluído com sucesso.")

    def excluir_hotel(self, nome: str):
        for h in self.__hoteis:
            if h.nome == nome:
                self.__hoteis.remove(h)
                print(f"✅ Hotel '{nome}' excluído.")
                return
        print(f"⚠️ Hotel '{nome}' não encontrado.")

    def alterar_hotel(self, nome: str, novos_dados: dict):
        for h in self.__hoteis:
            if h.nome == nome:
                for chave, valor in novos_dados.items():
                    if hasattr(h, chave):
                        setattr(h, chave, valor)
                print(f"✅ Hotel '{nome}' alterado.")
                return
        print(f"⚠️ Hotel '{nome}' não encontrado.")

    def listar_hoteis(self) -> List[str]:
        return [f"{h.nome} - {len(h.quartos)} quartos - {len(h.hospedes)} hóspedes" for h in self.__hoteis]

    def buscar_hotel(self, nome: str) -> Hotel:
        for h in self.__hoteis:
            if h.nome == nome:
                return h
        return None
