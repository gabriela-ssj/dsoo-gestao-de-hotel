from telas.tela_abstrata_gui import TelaAbstrataGUI
import FreeSimpleGUI as sg
from typing import Optional, Dict, Any, List


class TelaServicoDeQuarto(TelaAbstrataGUI):

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
        sg.ChangeLookAndFeel('LightBlue6')
        layout = [
            [sg.Text('-------- MENU SERVIÇO DE QUARTO ----------', font=("Helvica", 25))],
            [sg.Text('Escolha sua opção', font=("Helvica", 15))],
            [sg.Radio('Solicitar Serviço', "RD1", key='1', enable_events=True)],
            [sg.Radio('Listar Serviços', "RD1", key='2', enable_events=True)],
            [sg.Radio('Alterar Status de Serviço', "RD1", key='3', enable_events=True)],
            [sg.Radio('Retornar', "RD1", key='0', default=True, enable_events=True)],
            [sg.Button('Confirmar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]
        self.__window = sg.Window('Gerenciar Serviços de Quarto', layout, finalize=True)

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

    def pega_dados_servico(self) -> Optional[Dict[str, Any]]:
        sg.ChangeLookAndFeel('LightGreen')
        
        tipos_servico = ["Limpeza Extra", "Toalhas", "Roupas de Cama", "Minibar", "Outro"]

        layout = [
            [sg.Text('--- SOLICITAR NOVO SERVIÇO ---', font=("Helvica", 20))],
            [sg.Text('Número do Quarto (ex: 101):', size=(25, 1)), sg.InputText('', key='numero_quarto')],
            [sg.Text('CPF do Funcionário:', size=(25, 1)), sg.InputText('', key='cpf_funcionario')],
            [sg.Text('Tipo de Serviço:', size=(25, 1)), sg.Combo(tipos_servico, default_value=tipos_servico[0], key='tipo_servico', readonly=False)],
            [sg.Text('Valor do Serviço (R$):', size=(25, 1)), sg.InputText('', key='valor')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Dados do Serviço', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar':
            try:
                numero_quarto = values['numero_quarto'].strip()
                cpf_funcionario = values['cpf_funcionario'].strip()
                tipo_servico = values['tipo_servico'].strip()
                valor_str = values['valor'].replace(',', '.').strip()

                if not numero_quarto or not cpf_funcionario or not tipo_servico or not valor_str:
                    raise ValueError("Todos os campos devem ser preenchidos.")
                
                if not cpf_funcionario.isdigit():
                    raise ValueError("O CPF deve conter apenas números.")
                
                valor = float(valor_str)
                if valor < 0:
                    raise ValueError("O valor do serviço não pode ser negativo.")

                return {
                    "numero_quarto": numero_quarto,
                    "cpf_funcionario": cpf_funcionario,
                    "tipo_servico": tipo_servico,
                    "valor": valor
                }

            except ValueError as e:
                self.mostra_mensagem(f"Erro nos dados: {e}")
                return None
            except Exception as e:
                self.mostra_mensagem(f"Erro inesperado ao coletar dados: {e}")
                return None
        
        return None

    def seleciona_servico(self) -> Optional[str]:
        sg.ChangeLookAndFeel('DarkBlue2')
        layout = [
            [sg.Text('--- SELECIONAR SERVIÇO ---', font=("Helvica", 20))],
            [sg.Text('Digite o Número do Quarto (para localizar o serviço):', font=("Helvica", 12))],
            [sg.InputText('', key='identificador')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Localizar Serviço', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar' and values['identificador'].strip():
            return values['identificador'].strip()
        
        return None

    def seleciona_status(self) -> Optional[str]:
        sg.ChangeLookAndFeel('DarkPurple2')
        
        opcoes_status = ["solicitado", "em andamento", "concluído", "interrompido"]
        
        layout = [
            [sg.Text('Selecione o novo status:', font=("Helvica", 15))],
            [sg.Frame('', [
                [sg.Radio(s.capitalize(), "STATUS", key=s, default=(s == "solicitado"))] for s in opcoes_status
            ], border_width=0)],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Alterar Status', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar':
            for status in opcoes_status:
                if values.get(status):
                    return status
            self.mostra_mensagem("Nenhum status selecionado.")
            return None
        return None

    def mostra_lista(self, lista_servicos: List[Dict[str, Any]]):
        if not lista_servicos:
            self.mostra_mensagem("Nenhum serviço de quarto cadastrado.")
            return

        headings = ['Quarto', 'Funcionário', 'Tipo', 'Valor (R$)', 'Status']
        
        data = []
        for servico in lista_servicos:
            valor_formatado = f"{servico.get('valor', 0.0):.2f}".replace('.', ',')
            data.append([
                servico.get('numero_quarto', 'N/A'), 
                servico.get('nome_funcionario', 'N/A'), 
                servico.get('tipo_servico', 'N/A'), 
                valor_formatado,
                servico.get('status', 'N/A').capitalize() 
            ])
        
        sg.ChangeLookAndFeel('SystemDefault1')
        layout = [
            [sg.Text('--- SERVIÇOS DE QUARTO ---', font=("Helvica", 25))],
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
        
        self.__window = sg.Window('Lista de Serviços', layout, finalize=True)
        self.open() 
        self.close()