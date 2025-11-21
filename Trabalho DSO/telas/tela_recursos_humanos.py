from telas.tela_abstrata_gui import TelaAbstrataGUI
import FreeSimpleGUI as sg
from typing import Optional, List, Dict, Any


class TelaRh(TelaAbstrataGUI):

    def __init__(self):
        self.__window = None

    def mostra_mensagem(self, msg: str):
        sg.popup_ok(msg, font=("Helvica", 12))

    def close(self):
        if self.__window:
            self.__window.close()
        self.__window = None

    def open(self):
        if self.__window:
            button, values = self.__window.read()
            return button, values
        return None, None

    def tela_opcoes(self) -> int:
        sg.ChangeLookAndFeel('DarkBrown3')
        layout = [
            [sg.Text('-------- MENU RH ----------', font=("Helvica", 25))],
            [sg.Text('Escolha o subsistema:', font=("Helvica", 15))],
            [sg.Radio('Gerenciar Cargos', "RD1", key='1', enable_events=True)],
            [sg.Radio('Gerenciar Funcionários', "RD1", key='2', enable_events=True)],
            [sg.Radio('Retornar', "RD1", key='0', default=True, enable_events=True)],
            [sg.Button('Confirmar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]
        self.__window = sg.Window('Recursos Humanos', layout, finalize=True)

        opcao_selecionada = 0
        while True:
            event, values = self.open()

            if event in (None, 'Cancelar'):
                opcao_selecionada = 0
                break

            if event == 'Confirmar':
                for key in ['1', '2', '0']:
                    if values.get(key):
                        opcao_selecionada = int(key)
                        break
                break

        self.close()
        return opcao_selecionada

    def pega_metodo_pagamento(self) -> Optional[str]:
        sg.ChangeLookAndFeel('DarkBlue7')
        
        opcoes_pagamento = ['Pix', 'Transferência Bancária', 'Cheque', 'Outro']

        layout = [
            [sg.Text('--- MÉTODO DE PAGAMENTO ---', font=("Helvica", 20))],
            [sg.Text('Método de pagamento:', size=(20, 1)), 
             sg.Combo(opcoes_pagamento, default_value=opcoes_pagamento[0], key='metodo', readonly=False)],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Método de Pagamento', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar' and values['metodo'].strip():
            return values['metodo'].strip()
        
        return None

    def mostra_lista(self, lista_dados: List[Dict[str, Any]]):
        if not lista_dados:
            self.mostra_mensagem("Nenhum item cadastrado para listar.")
            return

        if isinstance(lista_dados[0], dict):

            headings = list(lista_dados[0].keys())
            data = [list(item.values()) for item in lista_dados]
        else:
            self.mostra_mensagem("A listagem de dados ainda está no formato de texto simples.")
            for item in lista_dados:
                 self.mostra_mensagem(item)
            return

        sg.ChangeLookAndFeel('GrayGrayGray')
        layout = [
            [sg.Text('--- LISTA DE DADOS RH ---', font=("Helvica", 25))],
            [sg.Table(values=data, 
                      headings=headings, 
                      auto_size_columns=True, 
                      display_row_numbers=False, 
                      justification='left', 
                      num_rows=min(25, len(data)), 
                      key='-TABLE-',
                      row_height=25)],
            [sg.Button('Fechar')]
        ]
        
        self.__window = sg.Window('Listagem RH', layout, finalize=True)
        self.open() 
        self.close()
