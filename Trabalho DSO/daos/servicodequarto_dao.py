from daos.dao import DAO
from entidades.servico_de_quarto import ServicoDeQuarto

class ServicoDeQuartoDAO(DAO):
    def __init__(self):
        super().__init__('servicos.pkl')

    def add(self, servico: ServicoDeQuarto):
        if (
            servico is not None 
            and isinstance(servico, ServicoDeQuarto) 
            and isinstance(servico.quarto.numero, int)
        ):
            super().add(servico.quarto.numero, servico)

    def update(self, servico: ServicoDeQuarto):
        if (
            servico is not None 
            and isinstance(servico, ServicoDeQuarto) 
            and isinstance(servico.quarto.numero, int)
        ):
            super().update(servico.quarto.numero, servico)

    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
