from telas.tela_abstrata_gui import TelaAbstrataGUI
import FreeSimpleGUI as sg
from typing import Optional, List, Dict, Any


class TelaSistemaHotel(TelaAbstrataGUI): 
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
        Exibe a tela de opções do Sistema de Hotéis e retorna a opção selecionada.
        """
        self.init_opcoes()
        opcao_selecionada = 0

        while True:
            event, values = self.open() 
            if event in (None, 'Cancelar'):
                opcao_selecionada = 0
                break

            if event == 'Confirmar':
                for key in ['1', '2', '3', '4', '5', '0']:
                    if values.get(key):
                        opcao_selecionada = int(key)
                        break
                break
                
        self.close()
        return opcao_selecionada

    def init_opcoes(self):
        """ Cria o layout da janela de opções do Sistema de Hotéis. """
        sg.ChangeLookAndFeel('DarkBlue3') 
        
        layout = [
            [sg.Text('-------- SISTEMA DE HOTÉIS ----------', font=("Helvica", 20))],
            [sg.Text('Escolha sua opção:', font=("Helvica", 15))],
            [sg.Radio('Incluir Hotel', "RD1", key='1', enable_events=True)], 
            [sg.Radio('Alterar Hotel', "RD1", key='2', enable_events=True)],
            [sg.Radio('Listar Hotéis', "RD1", key='3', enable_events=True)],
            [sg.Radio('Excluir Hotel', "RD1", key='4', enable_events=True)],
            [sg.Radio('Acessar Hotel', "RD1", key='5', enable_events=True)],
            [sg.Radio('Retornar', "RD1", key='0', default=True, enable_events=True)],
            [sg.Button('Confirmar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]
        
        self.__window = sg.Window('Gerenciar Hotéis', layout, finalize=True)

    def pega_dados_hotel(self) -> Optional[Dict[str, str]]:
        """ Coleta o nome do hotel para inclusão ou alteração. """
        sg.ChangeLookAndFeel('DarkTeal4')
        
        layout = [
            [sg.Text('-------- DADOS DO HOTEL ----------', font=("Helvica", 20))],
            [sg.Text('Nome do hotel:', size=(15, 1)), sg.InputText('', key='nome_hotel')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        
        self.__window = sg.Window('Dados do Hotel', layout, finalize=True)
        button, values = self.open()
        self.close()

        if button == 'Confirmar' and values['nome_hotel'].strip():
            nome = values['nome_hotel'].strip()
            return {"nome": nome}
        return None

    def seleciona_hotel(self) -> Optional[str]:
        """ Solicita o nome do hotel para acessar, alterar ou excluir. """
        sg.ChangeLookAndFeel('DarkBlue3')
        
        layout = [
            [sg.Text('-------- SELECIONAR HOTEL ----------', font=("Helvica", 20))],
            [sg.Text('Digite o nome do hotel:', font=("Helvica", 12))],
            [sg.InputText('', key='nome_selecionado')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        
        self.__window = sg.Window('Selecionar Hotel', layout, finalize=True)
        button, values = self.open()
        self.close()

        if button == 'Confirmar' and values['nome_selecionado'].strip():
            return values['nome_selecionado'].strip()
        return None

    def mostra_lista(self, lista: List[str]):
        """ Exibe a lista de hotéis em um campo de texto não editável. """
        
        if not lista:
            conteudo = "Nenhum hotel cadastrado."
        else:
            conteudo = "--- HOTÉIS CADASTRADOS ---\n\n"
            conteudo += "\n".join(lista)

        sg.ChangeLookAndFeel('LightBlue4')
        layout = [
            [sg.Text('Lista de Hotéis', font=("Helvica", 16))],
            [sg.Multiline(conteudo, size=(50, 10), disabled=True)],
            [sg.Button('OK')]
        ]
        
        self.__window = sg.Window('Lista de Hotéis', layout, finalize=True)
        self.open()
        self.close()
