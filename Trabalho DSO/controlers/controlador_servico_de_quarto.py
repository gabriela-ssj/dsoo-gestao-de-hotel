from entidades.servico_de_quarto import ServicoDeQuarto
from telas.tela_servico_de_quarto import TelaServicoDeQuarto

from controlers.controlador_hospede import ControladorHospede
from controlers.controlador_quartos import ControladorQuartos  
from controlers.controlador_funcionario import ControladorFuncionario

class ControladorServicoDeQuarto:
    def __init__(self):
        self.__tela = TelaServicoDeQuarto()
        self.__controlador_hospede = ControladorHospede()
        self.__controlador_quarto = ControladorQuartos()
        self.__controlador_funcionario = ControladorFuncionario()
        self.__servicos = []
        self.tela_aberta = False