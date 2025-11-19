from telas.tela_abstrata_gui import TelaAbstrataGUI
import FreeSimpleGUI as sg
from typing import Optional, Dict, Any, List


class TelaPagamento(TelaAbstrataGUI):
    
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
        sg.ChangeLookAndFeel('DarkBlue2')
        layout = [
            [sg.Text('-------- MENU PAGAMENTO ----------', font=("Helvica", 25))],
            [sg.Text('Escolha sua opção', font=("Helvica", 15))],
            [sg.Radio('Realizar Pagamento para Reserva', "RD1", key='1', enable_events=True)],
            [sg.Radio('Alterar Método de Pagamento', "RD1", key='2', enable_events=True)],
            [sg.Radio('Exibir Comprovante de Pagamento', "RD1", key='3', enable_events=True)],
            [sg.Radio('Retornar', "RD1", key='0', default=True, enable_events=True)],
            [sg.Button('Confirmar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]
        self.__window = sg.Window('Gerenciar Pagamentos', layout, finalize=True)

        opcao_selecionada = 0
        while True:
            event, values = self.open()

            if event in (None, 'Cancelar'):
                opcao_selecionada = 0
                break

            if event == 'Confirmar':
                for key in ['1', '2', '3', '0']:
                    if values.get(key):
                        opcao_selecionada = int(key)
                        break
                break

        self.close()
        return opcao_selecionada

    def pega_valor_pagamento(self) -> Optional[float]:
        sg.ChangeLookAndFeel('LightBrown4')
        layout = [
            [sg.Text('Digite o valor a ser pago:', font=("Helvica", 12))],
            [sg.InputText('', key='valor_pago')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Valor do Pagamento', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar':
            valor_str = values['valor_pago'].replace(',', '.').strip()
            try:
                valor = float(valor_str)
                if valor <= 0:
                    self.mostra_mensagem("O valor deve ser positivo.")
                    return None
                return valor
            except ValueError:
                self.mostra_mensagem("Valor inválido. Use apenas números.")
                return None
        return None

    def pega_metodo_pagamento(self) -> Optional[str]:
        sg.ChangeLookAndFeel('LightBrown4')

        metodos = ["Credito", "Debito", "Dinheiro", "Pix", "Transferencia"]
        
        layout = [
            [sg.Text('Selecione o novo método de pagamento:', font=("Helvica", 12))],
            [sg.Frame('', [
                [sg.Radio(m, "METODO", key=m, default=(m == "Credito"))] for m in metodos
            ], border_width=0)],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Método de Pagamento', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar':
            for metodo in metodos:
                if values.get(metodo):
                    return metodo
            self.mostra_mensagem("Nenhum método de pagamento selecionado.")
            return None
        return None

    def seleciona_reserva_para_pagamento(self) -> Optional[int]:
        sg.ChangeLookAndFeel('DarkBlue3')
        layout = [
            [sg.Text('--- SELECIONAR RESERVA/PAGAMENTO ---', font=("Helvica", 20))],
            [sg.Text('Digite o ID da Reserva/Pagamento:', size=(25, 1))],
            [sg.InputText('', key='id_selecionado')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Selecionar ID', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar' and values['id_selecionado'].strip():
            id_str = values['id_selecionado'].strip()
            try:
                reserva_id = int(id_str)
                if reserva_id <= 0:
                     self.mostra_mensagem("O ID deve ser um número positivo.")
                     return None
                return reserva_id
            except ValueError:
                self.mostra_mensagem("ID inválido. Digite um número inteiro.")
                return None
        return None

    def mostra_comprovante(self, comprovante_dados: Dict[str, Any]):
        sg.ChangeLookAndFeel('LightGreen')

        comprovante_linhas = []
        for key, value in comprovante_dados.items():
            key_formatada = key.replace('_', ' ').capitalize()
            if isinstance(value, list):
                comprovante_linhas.append(f"{key_formatada}:")
                for item in value:
                    comprovante_linhas.append(f"  - {item}")
            else:
                if isinstance(value, (float, int)) and 'valor' in key.lower():
                    value_str = f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                else:
                    value_str = str(value)
                    
                comprovante_linhas.append(f"{key_formatada}: {value_str}")

        comprovante_text = "\n".join(comprovante_linhas)

        layout = [
            [sg.Text('--- COMPROVANTE DE PAGAMENTO ---', font=("Helvica", 25))],
            [sg.Multiline(comprovante_text, 
                          size=(50, 15), 
                          key='-COMPROVANTE-', 
                          disabled=True, 
                          background_color='#f0f0f0', 
                          text_color='black', 
                          font=('Courier', 11))],
            [sg.Button('Fechar')]
        ]
        
        self.__window = sg.Window('Comprovante de Pagamento', layout, finalize=True)
        self.open()
        self.close()
