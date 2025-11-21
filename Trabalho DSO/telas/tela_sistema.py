from telas.tela_abstrata_gui import TelaAbstrataGUI
import FreeSimpleGUI as sg
from typing import Optional, Dict, Any


class TelaSistema(TelaAbstrataGUI): 
    def __init__(self):
        self.__window = None 

    def mostra_mensagem(self, msg: str):
        """ Exibe uma mensagem em um popup de confirmação. """
        sg.popup_ok(msg, font=("Helvica", 12))

    def close(self):
        """ Fecha a janela atual. """
        if self.__window:
            self.__window.close() 
        self.__window = None

    def open(self):
        """ Abre a janela e retorna o botão/evento e os valores lidos. """
        if self.__window:
            button, values = self.__window.read() 
            return button, values
        return None, None

    def tela_opcoes(self) -> int:
        """ 
        Exibe a tela de opções principal do sistema e retorna a opção selecionada (1 ou 0).
        """
        self.init_opcoes()
        opcao_selecionada = 0

        while True:
            event, values = self.open() 
            if event in (None, 'Cancelar'):
                opcao_selecionada = 0
                break

            if event == 'Confirmar':
                for key in ['1', '0']:
                    if values.get(key):
                        opcao_selecionada = int(key)
                        break
                break
                
        self.close()
        return opcao_selecionada

    def init_opcoes(self):
        """ Cria o layout da janela de opções do Menu Principal. """
        sg.ChangeLookAndFeel('DarkBlue3')
        
        layout = [
            [sg.Text('-------- MENU PRINCIPAL DO SISTEMA DE HOTÉIS ----------', font=("Helvica", 20))],
            [sg.Text('Escolha sua opção:', font=("Helvica", 15))],
            [sg.Radio('Gerenciar Hotéis', "RD1", key='1', enable_events=True)], 
            [sg.Radio('Sair do sistema', "RD1", key='0', default=True, enable_events=True)],
            [sg.Button('Confirmar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]
        
        self.__window = sg.Window('Sistema de Hotéis', layout, finalize=True)
