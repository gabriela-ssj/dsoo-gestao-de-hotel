from daos.dao import DAO
from entidades.recursos_humanos import Rh

class RhDAO(DAO):
    def __init__(self):
        super().__init__('rh.pkl')

    def add(self, rh: Rh):
        if isinstance(rh, Rh):
            super().add("rh", rh)   

    def update(self, rh: Rh):
        if isinstance(rh, Rh):
            super().update("rh", rh)

    def get(self):
        return super().get("rh")

    def remove(self):
        return super().remove("rh")
