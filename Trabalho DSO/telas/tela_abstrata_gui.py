from abc import ABC, abstractmethod
import FreeSimpleGUI as sg
from typing import Optional, Any, Tuple

class TelaAbstrataGUI(ABC):
    """
    Classe Abstrata para Telas de Interface Gráfica (GUI) usando FreeSimpleGUI.
    """
    def __init__(self):
        self.__window: Optional[sg.Window] = None 
        sg.theme('DarkBlue3') 

    def open(self) -> Tuple[Any, Optional[dict]]:
        """Abre e lê eventos da janela atual do FreeSimpleGUI."""
        if self.__window:
            return self.__window.read() 
        return None, None

    def close(self):
        """Fecha a janela atual do FreeSimpleGUI."""
        if self.__window:
            self.__window.close() 
        self.__window = None

    def mostra_mensagem(self, msg: str):
        """Exibe uma mensagem em um popup do FreeSimpleGUI (substitui o print)."""
        sg.popup_ok(msg, title="Atenção", font=("Helvica", 12))

    def confirma_acao(self, mensagem: str, titulo: str = "Confirmar Ação") -> bool:
        """Exibe um popup de confirmação Sim/Não."""
        confirmacao = sg.popup_yes_no(mensagem, title=titulo, font=("Helvica", 12))
        return confirmacao == 'Yes'

    @abstractmethod
    def tela_opcoes(self) -> int:
        """Deve exibir o menu de opções da tela e retornar a opção escolhida."""
        pass