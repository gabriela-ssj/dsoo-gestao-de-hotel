from telas.tela_abstrata_gui import TelaAbstrataGUI
import FreeSimpleGUI as sg
from typing import Optional, List, Dict, Any

class TelaHotel(TelaAbstrataGUI):

    def __init__(self):
        self.__window = None

    def mostra_mensagem(self, msg: str):
        """Exibe uma mensagem em um popup do FreeSimpleGUI."""
        sg.popup_ok(msg, font=("Helvica", 12))

    def close(self):
        """Fecha a janela atual do FreeSimpleGUI."""
        if self.__window:
            self.__window.close()
        self.__window = None

    def open(self):
        """Lê a janela e retorna o evento e os valores."""
        if self.__window:
            button, values = self.__window.read()
            return button, values
        return None, None

    def tela_opcoes(self) -> int:
        """Exibe o menu principal do Hotel e retorna a escolha do usuário (0-7)."""
        sg.ChangeLookAndFeel('DarkTeal9')
        
        opcoes_menu = [
            (1, 'Cadastro de Hóspede'),
            (2, 'Gerenciar Quartos'),
            (3, 'Gerenciar Reservas'),
            (4, 'Pagamentos'),
            (5, 'Recursos Humanos'),
            (6, 'Relatório: Quartos mais reservados'),
            (7, 'Gerenciar Serviços de Quarto'),
            (0, 'Retornar ao menu anterior')
        ]
        
        radio_buttons = []
        for key, description in opcoes_menu:
            is_default = (key == 0)
            radio_buttons.append(
                sg.Radio(description, "MENU_OPCOES", key=str(key), default=is_default, enable_events=True)
            )

        layout = [
            [sg.Text('-------- MENU DO HOTEL --------', font=("Helvica", 25))],
            [sg.Text('Selecione uma opção para continuar:', font=("Helvica", 15))],
            [sg.Column([
                [rb] for rb in radio_buttons
            ], pad=(10, 10))],
            [sg.Button('Confirmar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]
        
        self.__window = sg.Window('Menu Principal do Hotel', layout, finalize=True)

        opcao_selecionada = 0
        while True:
            event, values = self.open()

            if event in (None, 'Cancelar'):
                opcao_selecionada = 0
                break

            if event == 'Confirmar':
                for key, _ in opcoes_menu:
                    str_key = str(key)
                    if values.get(str_key):
                        opcao_selecionada = key
                        break
                break

        self.close()
        return opcao_selecionada

    def mostra_lista(self, lista_dados: List[Dict[str, Any]]):
        """
        Exibe uma lista de dados (ex: Relatório) em formato de tabela gráfica.
        
        Nota: Esta função agora espera uma Lista de Dicionários (List[Dict])
        para construir a tabela GUI, assim como nas outras Views corrigidas.
        """
        if not lista_dados:
            self.mostra_mensagem("Nenhum dado para listar.")
            return

        if isinstance(lista_dados[0], dict):
            headings = list(lista_dados[0].keys())
            data = [list(item.values()) for item in lista_dados]
        else:
            self.mostra_mensagem("Exibindo lista simples (Relatório):")
            headings = ['Dados']
            data = [[item] for item in lista_dados]
        
        sg.ChangeLookAndFeel('SystemDefault')
        layout = [
            [sg.Text('--- LISTA DE DADOS ---', font=("Helvica", 25))],
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
        
        self.__window = sg.Window('Listagem do Hotel', layout, finalize=True)
        self.open() 
        self.close()
