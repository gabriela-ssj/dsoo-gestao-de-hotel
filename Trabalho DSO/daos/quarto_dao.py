from daos.dao import DAO
from entidades.quarto import Quarto


class QuartoDAO(DAO):
    def __init__(self):
        super().__init__('quartos.pkl')

    def add(self, quarto: Quarto):
        if quarto is not None and isinstance(quarto, Quarto) and isinstance(quarto.numero, int):
            super().add(quarto.numero, quarto)

    def update(self, quarto: Quarto):
        if quarto is not None and isinstance(quarto, Quarto) and isinstance(quarto.numero, int):
            super().update(quarto.numero, quarto)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
