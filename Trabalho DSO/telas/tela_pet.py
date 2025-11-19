from telas.tela_abstrata_gui import TelaAbstrataGUI # Assumindo a nova base GUI
import FreeSimpleGUI as sg
from typing import Optional, Dict, Any, List, Tuple
from controlers.ValidacaoException import ValidacaoException # Mantida para validação de regras de negócio


class TelaPet(TelaAbstrataGUI): 
    
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
        sg.ChangeLookAndFeel('Green')
        layout = [
            [sg.Text('-------- MENU PETS ----------', font=("Helvica", 25))],
            [sg.Text('Escolha sua opção', font=("Helvica", 15))],
            [sg.Radio('Cadastrar Pet', "RD1", key='1', enable_events=True)], 
            [sg.Radio('Listar Pets do Hóspede', "RD1", key='2', enable_events=True)],
            [sg.Radio('Remover Pet', "RD1", key='3', enable_events=True)],
            [sg.Radio('Alterar Pet', "RD1", key='4', enable_events=True)],
            [sg.Radio('Retornar', "RD1", key='0', default=True, enable_events=True)],
            [sg.Button('Confirmar', size=(10, 1)), sg.Button('Cancelar', size=(10, 1))]
        ]
        self.__window = sg.Window('Gerenciar Pets', layout, finalize=True)

    def pega_dados_pet(self, dados_atuais: Optional[Dict[str, str]] = None) -> Optional[Dict[str, str]]:
        sg.ChangeLookAndFeel('LightBlue2')
        dados_atuais = dados_atuais or {}
        
        nome_val = dados_atuais.get('nome_pet', '')
        especie_val = dados_atuais.get('especie', '')

        layout = [
            [sg.Text('--- DADOS DO PET ---', font=("Helvica", 20))],
            [sg.Text('Nome do Pet:', size=(15, 1)), sg.InputText(nome_val, key='nome_pet')], 
            [sg.Text('Espécie:', size=(15, 1)), sg.InputText(especie_val, key='especie')], 
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Dados do Pet', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar':
            nome_pet = values['nome_pet'].strip()
            especie = values['especie'].strip()

            try:
                ValidacaoException.validar_campo_vazio(nome_pet, "Nome do Pet")
                ValidacaoException.validar_campo_vazio(especie, "Espécie")
                
                return {"nome_pet": nome_pet, "especie": especie}

            except ValidacaoException as e:
                self.mostra_mensagem(f"Erro de Validação: {e}")
                return None
        
        return None
    
    def seleciona_pet(self) -> Optional[Tuple[str, str]]:
        sg.ChangeLookAndFeel('DarkBlue3')
        layout = [
            [sg.Text('--- SELECIONAR PET ---', font=("Helvica", 20))],
            [sg.Text('CPF do Tutor (11 dígitos):', size=(20, 1)), sg.InputText('', key='cpf_hospede')],
            [sg.Text('Nome do Pet:', size=(20, 1)), sg.InputText('', key='nome_pet')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        self.__window = sg.Window('Selecionar Pet', layout, finalize=True)

        button, values = self.open()
        self.close()

        if button == 'Confirmar':
            cpf_hospede = values['cpf_hospede'].strip()
            nome_pet = values['nome_pet'].strip()

            try:
                if not cpf_hospede.isdigit() or len(cpf_hospede) != 11:
                    raise ValidacaoException("CPF do tutor inválido! Deve conter 11 dígitos.")

                ValidacaoException.validar_campo_vazio(nome_pet, "Nome do Pet")
                
                return cpf_hospede, nome_pet

            except ValidacaoException as e:
                self.mostra_mensagem(f"Erro de Validação: {e}")
                return None
        
        return None

    def mostra_lista(self, dados_pets: List[Dict[str, Any]], nome_tutor: str):
        headings = ['Nome do Pet', 'Espécie']

        data = []
        for pet in dados_pets:
            data.append([
                pet.get('nome', 'N/A'), 
                pet.get('especie', 'N/A') 
            ])
        
        if not data:
            self.mostra_mensagem(f"O hóspede {nome_tutor} não possui pets cadastrados.")
            return

        sg.ChangeLookAndFeel('LightGreen')
        layout = [
            [sg.Text(f'-- PETS DO HÓSPEDE: {nome_tutor.upper()} --', font=("Helvica", 25))],
            [sg.Table(values=data, 
                      headings=headings, 
                      auto_size_columns=True, 
                      display_row_numbers=False, 
                      justification='left', 
                      num_rows=min(15, len(data)), 
                      key='-TABLE-',
                      row_height=25)],
            [sg.Button('Fechar')]
        ]
        
        self.__window = sg.Window('Lista de Pets', layout, finalize=True)
        self.open() 
        self.close()

    def confirma_acao(self, mensagem: str) -> bool:
        confirmacao = sg.popup_yes_no(mensagem, title="Confirmar Ação", font=("Helvica", 12))
        return confirmacao == 'Yes'
