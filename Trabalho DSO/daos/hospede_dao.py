from daos.dao import DAO
from entidades.hospede import Hospede

class HospedeDAO(DAO):
    def __init__(self):
        super().__init__("hospedes.pkl")

    def add(self, hospede: Hospede):
        if hospede is not None and isinstance(hospede, Hospede) and isinstance(hospede.cpf, str):
            super().add(hospede.cpf, hospede)

    def update(self, hospede: Hospede):
        if hospede is not None and isinstance(hospede, Hospede) and isinstance(hospede.cpf, str):
            super().update(hospede.cpf, hospede)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)
