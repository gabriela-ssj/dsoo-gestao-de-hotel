from telas.tela_abstrata_gui import TelaAbstrataGUI
import FreeSimpleGUI as sg
from typing import Optional, Dict, Any, List


class TelaQuarto(TelaAbstrataGUI):

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
        sg.ChangeLookAndFeel('DarkRed')
        layout = [
            [sg.Text('------ MENU QUARTOS ------', font=("Helvica", 25))],
            [sg.Text('Escolha sua opção', font=("Helvica", 15))],
            [sg.Radio('Cadastrar Quarto', "RD1", key='1', enable_events=True)],
            [sg.Radio('Listar Quartos', "RD1", key='2', enable_events=True)],
            [sg.Radio('Alterar Quarto', "RD1", key='3', enable_events=True)],
            [sg.Radio('Excluir Quarto', "RD1", key='4', enable_events=True)],
            [sg.Radio('Retornar', "RD1", key='0', default=True, enable_events=True)],
            [sg.Button('Confirmar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]
        self.__window = sg.Window('Gerenciar Quartos', layout, finalize=True)

        opcao_selecionada = 0
        while True:
            event, values = self.open()

            if event in (None, 'Cancelar'):
                opcao_selecionada = 0
                break

            if event == 'Confirmar':
                for key in ['1', '2', '3', '4', '0']:
                    if values.get(key):
                        opcao_selecionada = int(key)
                        break
                break

        self.close()
        return opcao_selecionada

    def pega_dados_quarto(self, modo: str = None, dados_atuais: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        sg.ChangeLookAndFeel('DarkTeal3') 
        
        dados_atuais = dados_atuais or {}

        numero_val = str(dados_atuais.get('numero', ''))
        tipo_existente = dados_atuais.get('tipo', 'simples')
        disponibilidade_val = dados_atuais.get('disponibilidade', True)
        hidro_val = dados_atuais.get('hidro', False)
        
        titulo = "CADASTRAR NOVO QUARTO" if modo != "alt" else f"ALTERAR QUARTO {numero_val}"
    
        layout = [
            [sg.Text(titulo, font=("Helvica", 20))],
            [sg.Text('Número do Quarto:', size=(20, 1)), sg.InputText(numero_val, key='numero', disabled=(modo == "alt"))] 
        ]

        if modo != "alt":
            layout.append([sg.Text('Tipo do Quarto:', size=(20, 1)), 
                           sg.Combo(['simples', 'duplo', 'suite'], default_value='simples', key='tipo', enable_events=True)])

            layout.append([sg.Frame('Acessórios', [
                [sg.Checkbox('Possui Hidromassagem?', key='hidro', default=hidro_val)]
            ], key='HIDRO_FRAME', visible=(tipo_existente == 'suite'), border_width=0)])

        if modo == "alt":
            layout.append([sg.Text(f'Tipo atual: {tipo_existente.upper()}', font=('Helvica', 12))])

            layout.append([sg.Text('Disponível?', size=(20, 1)), 
                           sg.Combo(['sim', 'nao'], 
                                    default_value=('sim' if disponibilidade_val else 'nao'), 
                                    key='disponibilidade')])
                                    
            if tipo_existente == "suite":
                 layout.append([sg.Checkbox('Possui Hidromassagem?', key='hidro', default=hidro_val)])


        layout.append([sg.Button('Confirmar'), sg.Button('Cancelar')])

        self.__window = sg.Window('Dados do Quarto', layout, finalize=True)

        if modo != "alt":

            while True:
                event, values = self.open()

                if event == sg.WIN_CLOSED or event == 'Cancelar':
                    self.close()
                    return None

                if event == 'tipo':

                    self.__window['HIDRO_FRAME'].update(visible=(values['tipo'] == 'suite'))
                    self.__window.refresh()
                
                if event == 'Confirmar':
                    self.close()
                    break
        else:
            event, values = self.open()
            self.close()

        if event == 'Confirmar':
            try:
                numero_str = values['numero'].strip()
                if not numero_str or not numero_str.isdigit():
                    self.mostra_mensagem("Número do quarto inválido. Deve ser um número inteiro positivo.")
                    return None
                numero = int(numero_str)

                dados_retorno: Dict[str, Any] = {"numero": numero}

                if modo != "alt":
                    tipo = values['tipo']
                    dados_retorno["tipo"] = tipo
                    
                    if tipo == "suite":
                        dados_retorno["hidro"] = values['hidro']

                if modo == "alt":
                    disp_str = values['disponibilidade']
                    dados_retorno["disponibilidade"] = (disp_str == 'sim')

                    if tipo_existente == "suite":
                        dados_retorno["hidro"] = values['hidro'] # True/False
                
                return dados_retorno

            except Exception as e:
                self.mostra_mensagem(f"Erro ao processar dados: {e}")
                return None
                
        return None

    def seleciona_quarto(self) -> Optional[int]:
        sg.ChangeLookAndFeel('DarkBlue3')
        layout = [
            [sg.Text('--- SELECIONAR QUARTO ---', font=("Helvica", 20))],
            [sg.Text('Digite o número do quarto:', font=("Helvica", 12))],
            [sg.InputText('', key='numero_quarto')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Selecionar Quarto', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar' and values['numero_quarto'].strip():
            numero_str = values['numero_quarto'].strip()
            try:
                numero = int(numero_str)
                if numero <= 0:
                    self.mostra_mensagem("O número do quarto deve ser positivo.")
                    return None
                return numero
            except ValueError:
                self.mostra_mensagem("Número de quarto inválido. Digite um número inteiro.")
                return None
        return None

    def mostra_lista(self, dados_quartos: List[Dict[str, Any]]):
        headings = ['Número', 'Tipo', 'Disponível', 'Hidro', 'Hóspede Atual']
        
        data = []
        for quarto in dados_quartos:

            hidro_status = "Sim" if quarto.get('hidro') else "Não"
            disp_status = "Sim" if quarto.get('disponibilidade') else "Não"
            
            data.append([
                quarto.get('numero', 'N/A'), 
                quarto.get('tipo', 'N/A').capitalize(), 
                disp_status,
                hidro_status,
                quarto.get('hospede_nome', 'Vago') 
            ])
        
        if not data:
            self.mostra_mensagem("Nenhum quarto cadastrado.")
            return

        sg.ChangeLookAndFeel('LightGreen')
        layout = [
            [sg.Text('--- LISTA DE QUARTOS ---', font=("Helvica", 25))],
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
        
        self.__window = sg.Window('Lista de Quartos', layout, finalize=True)
        self.open() 
        self.close()
