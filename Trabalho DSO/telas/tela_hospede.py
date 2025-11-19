from telas.tela_abstrata_gui import TelaAbstrataGUI
import FreeSimpleGUI as sg
from typing import Optional, Dict, Any, List
from controlers.ValidacaoException import ValidacaoException
import re 


class TelaHospede(TelaAbstrataGUI): 
    
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
                for key in ['1', '2', '3', '4', '5', '0']:
                    if values.get(key):
                        opcao_selecionada = int(key)
                        break
                break 
        
        self.close()
        return opcao_selecionada

    def init_opcoes(self):
        sg.ChangeLookAndFeel('DarkBlue3')
        layout = [
            [sg.Text('-------- MENU HÓSPEDES ----------', font=("Helvica", 25))],
            [sg.Text('Escolha sua opção', font=("Helvica", 15))],
            [sg.Radio('Cadastrar Hóspede', "RD1", key='1', enable_events=True)], 
            [sg.Radio('Listar Hóspedes', "RD1", key='2', enable_events=True)],
            [sg.Radio('Excluir Hóspede', "RD1", key='3', enable_events=True)],
            [sg.Radio('Alterar Hóspede', "RD1", key='4', enable_events=True)],
            [sg.Radio('Gerenciar Pets do Hóspede', "RD1", key='5', enable_events=True)],
            [sg.Radio('Retornar', "RD1", key='0', default=True, enable_events=True)],
            [sg.Button('Confirmar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]
        self.__window = sg.Window('Gerenciar Hóspedes', layout, finalize=True)

    def pega_dados_hospede(self, modo: str = "cadastro", dados_atuais: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        sg.ChangeLookAndFeel('DarkTeal4')

        dados_atuais = dados_atuais or {}
        cpf_val = dados_atuais.get('cpf', '')
        nome_val = dados_atuais.get('nome', '')
        idade_val = str(dados_atuais.get('idade', ''))
        telefone_val = dados_atuais.get('telefone', '')
        email_val = dados_atuais.get('email', '')

        layout = [
            [sg.Text(f'-------- DADOS DO HÓSPEDE ({modo.upper()}) ----------', font=("Helvica", 25))],
            [sg.Text('CPF (11 dígitos):', size=(15, 1)), sg.InputText(cpf_val, key='cpf', disabled=(modo == "alteracao"))], 
            [sg.Text('Nome:', size=(15, 1)), sg.InputText(nome_val, key='nome')], 
            [sg.Text('Idade (>= 18):', size=(15, 1)), sg.InputText(idade_val, key='idade')],
            [sg.Text('Telefone:', size=(15, 1)), sg.InputText(telefone_val, key='telefone')],
            [sg.Text('E-mail:', size=(15, 1)), sg.InputText(email_val, key='email')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Dados do Hóspede', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar':
            cpf = values['cpf'].strip()
            nome = values['nome'].strip()
            idade_str = values['idade'].strip()
            telefone = values['telefone'].strip()
            email = values['email'].strip()

            try:

                if modo == "cadastro" or (modo == "alteracao" and not cpf):
                     if not cpf or not cpf.isdigit() or len(cpf) != 11:
                         raise ValidacaoException("CPF inválido! Deve conter 11 dígitos numéricos.")

                ValidacaoException.validar_campo_vazio(nome, "Nome")
                if not all(c.isalpha() or c.isspace() for c in nome): 
                    self.mostra_mensagem("O nome deve conter apenas letras e espaços.")
                    return None

                ValidacaoException.validar_campo_vazio(idade_str, "Idade")
                try:
                    idade = int(idade_str)
                except ValueError:
                    raise ValidacaoException("Idade deve ser um número inteiro.")
                ValidacaoException.validar_idade_valida(idade)

                ValidacaoException.validar_campo_vazio(telefone, "Telefone")
                if not telefone.isdigit() or not (8 <= len(telefone) <= 15):
                    self.mostra_mensagem("Telefone inválido! Use apenas números (8 a 15 dígitos).")
                    return None

                ValidacaoException.validar_email(email)

                return {
                    "cpf": cpf,
                    "nome": nome,
                    "idade": idade,
                    "telefone": telefone,
                    "email": email
                }

            except ValidacaoException as e:
                self.mostra_mensagem(f"Erro de Validação: {e}")
                return None
            except Exception as e:
                self.mostra_mensagem(f"Erro inesperado durante a validação: {e}")
                return None
                
        return None

    def seleciona_hospede(self) -> Optional[str]:
        sg.ChangeLookAndFeel('DarkBlue3')
        layout = [
            [sg.Text('-------- SELECIONAR HÓSPEDE ----------', font=("Helvica", 20))],
            [sg.Text('Digite o CPF do hóspede:', font=("Helvica", 12))],
            [sg.InputText('', key='cpf_selecionado')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Selecionar Hóspede', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar' and values['cpf_selecionado'].strip():
            cpf = values['cpf_selecionado'].strip()
            if cpf.isdigit() and len(cpf) == 11:
                return cpf
            else:
                self.mostra_mensagem("CPF inválido! Deve conter 11 dígitos numéricos.")
                return None
        return None

    def mostra_lista(self, dados_hospedes: List[Dict[str, Any]]):
        headings = ['Nome', 'CPF', 'Idade', 'Telefone', 'Email']

        data = []
        for hospede in dados_hospedes:
            data.append([
                hospede.get('nome', 'N/A'), 
                hospede.get('cpf', 'N/A'), 
                hospede.get('idade', 'N/A'),
                hospede.get('telefone', 'N/A'),
                hospede.get('email', 'N/A')
            ])
        
        if not data:
            self.mostra_mensagem("Nenhum hóspede cadastrado.")
            return

        sg.ChangeLookAndFeel('LightGreen')
        layout = [
            [sg.Text('-------- LISTA DE HÓSPEDES ----------', font=("Helvica", 25))],
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
        
        self.__window = sg.Window('Lista de Hóspedes', layout, finalize=True)
        self.open() 
        self.close()

    def confirma_acao(self, mensagem: str) -> bool:
        confirmacao = sg.popup_yes_no(mensagem, title="Confirmar Ação", font=("Helvica", 12))
        return confirmacao == 'Yes'
