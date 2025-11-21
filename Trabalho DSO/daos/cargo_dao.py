from daos.dao import DAO
from entidades.cargo import Cargo

class CargoDAO(DAO):
    def __init__(self):
        super().__init__("cargos.pkl")

    def add(self, cargo: Cargo):
        if cargo is not None and isinstance(cargo, Cargo) and isinstance(cargo.tipo_cargo, str):
            super().add(cargo.tipo_cargo.lower(), cargo)

    def update(self, cargo: Cargo):
        if cargo is not None and isinstance(cargo, Cargo) and isinstance(cargo.tipo_cargo, str):
            super().update(cargo.tipo_cargo.lower(), cargo)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key.lower())

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key.lower())
