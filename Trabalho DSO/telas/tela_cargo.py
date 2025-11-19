from telas.tela_abstrata_gui import TelaAbstrataGUI
import FreeSimpleGUI as sg
from typing import Dict, Any, Optional, List


class TelaCargo(TelaAbstrataGUI): 

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
        self.init_opcoes()
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

    def init_opcoes(self):
        sg.ChangeLookAndFeel('DarkBlue3')
        layout = [
            [sg.Text('-------- GESTÃO DE CARGOS ----------', font=("Helvica", 25))],
            [sg.Text('Escolha sua opção', font=("Helvica", 15))],
            [sg.Radio('Listar Cargos Disponíveis', "RD1", key='1', enable_events=True)], 
            [sg.Radio('Criar Cargo', "RD1", key='2', enable_events=True)],
            [sg.Radio('Alterar Cargo', "RD1", key='3', enable_events=True)],
            [sg.Radio('Excluir Cargo', "RD1", key='4', enable_events=True)],
            [sg.Radio('Retornar', "RD1", key='0', default=True, enable_events=True)],
            [sg.Button('Confirmar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]
        self.__window = sg.Window('Gerenciar Cargos', layout, finalize=True)

    def pega_dados_cargo(self, modo: str = "cadastro", nome_atual: Optional[str] = None, salario_atual: Optional[float] = None) -> Optional[Dict[str, Any]]:
        sg.ChangeLookAndFeel('DarkTeal4')

        nome_display = nome_atual if nome_atual else ""
        salario_display = f"{salario_atual:.2f}".replace('.', ',') if salario_atual is not None else ""
        
        titulo = f'-------- DADOS DO CARGO ({modo.upper()}) ----------'
        nome_label = f"Nome do Cargo ({'Atual: ' + nome_display if modo == 'alteracao' and nome_display else 'Obrigatório'}):"
        salario_label = f"Salário (R$) ({'Atual: R$' + salario_display if modo == 'alteracao' and salario_display else 'Obrigatório'}):"

        layout = [
            [sg.Text(titulo, font=("Helvica", 25))],
            [sg.Text(nome_label, size=(25, 1)), sg.InputText(nome_display, key='nome')], 
            [sg.Text(salario_label, size=(25, 1)), sg.InputText(salario_display, key='salario')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Dados do Cargo', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar':
            nome = values['nome'].strip()
            salario_str = values['salario'].strip().replace(',', '.')

            if not nome:
                if modo == "alteracao":
                    nome = nome_atual
                else:
                    self.mostra_mensagem("Nome do cargo é obrigatório no cadastro!")
                    return None

            salario = None
            if not salario_str:
                if modo == "alteracao" and salario_atual is not None:
                    salario = salario_atual
                else:
                    self.mostra_mensagem("Salário é obrigatório no cadastro!")
                    return None
            else:
                try:
                    salario = float(salario_str)
                    if salario <= 0:
                        self.mostra_mensagem("Salário inválido! Digite um número positivo.")
                        return None
                except ValueError:
                    self.mostra_mensagem("Salário inválido! Digite um número real positivo (use ponto ou vírgula).")
                    return None

            return {
                "nome": nome,
                "salario": salario
            }
            
        return None

    def seleciona_cargo(self) -> Optional[str]:
        sg.ChangeLookAndFeel('DarkBlue3')
        layout = [
            [sg.Text('-------- SELECIONAR CARGO ----------', font=("Helvica", 20))],
            [sg.Text('Digite o nome do cargo:', font=("Helvica", 12))],
            [sg.InputText('', key='nome_selecionado')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Selecionar Cargo', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar' and values['nome_selecionado'].strip():
            return values['nome_selecionado'].strip()
        return None

    def mostra_lista(self, lista_cargos: List[Dict[str, Any]]):
        headings = ['Nome', 'Salário (R$)']

        data = []
        for cargo in lista_cargos:
            salario_formatado = f"R$ {cargo.get('salario', 0.0):.2f}"
            data.append([cargo.get('nome', 'N/A'), salario_formatado])
        
        if not data:
            self.mostra_mensagem("Nenhum cargo cadastrado.")
            return

        sg.ChangeLookAndFeel('LightGreen')
        layout = [
            [sg.Text('-------- LISTA DE CARGOS ----------', font=("Helvica", 25))],
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
        
        self.__window = sg.Window('Lista de Cargos', layout, finalize=True)
        self.open() 
        self.close()

    def confirma_acao(self, mensagem: str) -> bool:
        confirmacao = sg.popup_yes_no(mensagem, title="Confirmar Ação", font=("Helvica", 12))
        return confirmacao == 'Yes'
