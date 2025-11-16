from telas.tela_abstrata import TelaAbstrata
import FreeSimpleGUI as sg
from typing import Optional, List, Dict, Any

class TelaFuncionario(TelaAbstrata):
  def __init__(self):
    self.__window = None

  def tela_opcoes(self) -> int:
    self.init_opcoes()
    button, values = self.open()
    
    opcao = 0
    if button == 'Confirmar':

        if values.get('1'):
            opcao = 1
        elif values.get('2'):
            opcao = 2
        elif values.get('3'):
            opcao = 3
        elif values.get('4'):
            opcao = 4
        elif values.get('0'):
            opcao = 0
    elif button in (None, 'Cancelar'):
        opcao = 0
    
    self.close()
    return opcao

  def init_opcoes(self):
    sg.ChangeLookAndFeel('DarkBlue3')
    layout = [
      [sg.Text('-------- FUNCIONÁRIOS ----------', font=("Helvica", 25))],
      [sg.Text('Escolha sua opção', font=("Helvica", 15))],
      [sg.Radio('Cadastrar Funcionário', "RD1", key='1')],
      [sg.Radio('Listar Funcionários', "RD1", key='2')],
      [sg.Radio('Alterar Funcionário', "RD1", key='3')],
      [sg.Radio('Excluir Funcionário', "RD1", key='4')],
      [sg.Radio('Retornar', "RD1", key='0', default=True)],
      [sg.Button('Confirmar'), sg.Button('Cancelar')]
    ]
    self.__window = sg.Window('Gerenciar Funcionários').Layout(layout)

  def pega_dados_funcionario(self, modo: str = "cadastro", dados_atuais: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
    sg.ChangeLookAndFeel('DarkTeal4')

    dados_atuais = dados_atuais or {}
    cpf_val = dados_atuais.get('cpf', '')
    nome_val = dados_atuais.get('nome', '')
    cargo_nome_val = dados_atuais.get('cargo_nome', '')
    salario_val = str(dados_atuais.get('salario', ''))
    idade_val = str(dados_atuais.get('idade', ''))
    telefone_val = dados_atuais.get('telefone', '')
    email_val = dados_atuais.get('email', '')

    layout = [
      [sg.Text(f'-------- DADOS FUNCIONÁRIO ({modo.upper()}) ----------', font=("Helvica", 25))],

      [sg.Text('Nome:', size=(15, 1)), sg.InputText(nome_val, key='nome')], 
      [sg.Text('CPF (11 dígitos):', size=(15, 1)), sg.InputText(cpf_val, key='cpf')],
      [sg.Text('Nome do Cargo:', size=(15, 1)), sg.InputText(cargo_nome_val, key='cargo_nome')],
      [sg.Text('Salário:', size=(15, 1)), sg.InputText(salario_val, key='salario')],
      [sg.Text('Idade:', size=(15, 1)), sg.InputText(idade_val, key='idade')],
      [sg.Text('Telefone:', size=(15, 1)), sg.InputText(telefone_val, key='telefone')],
      [sg.Text('E-mail:', size=(15, 1)), sg.InputText(email_val, key='email')],
      [sg.Button('Confirmar'), sg.Button('Cancelar')]
    ]
    self.__window = sg.Window('Dados do Funcionário').Layout(layout)

    button, values = self.open()
    self.close()

    if button == 'Confirmar':
      nome = values['nome'].strip()
      cpf = values['cpf'].strip()
      cargo_nome = values['cargo_nome'].strip()
      salario_str = values['salario'].strip()
      idade_str = values['idade'].strip()
      telefone = values['telefone'].strip()
      email = values['email'].strip()

      if not nome:
        self.mostra_mensagem("Nome é obrigatório!")
        return None
      if not cpf or not cpf.isdigit() or len(cpf) != 11:
        self.mostra_mensagem("CPF inválido! Deve conter 11 dígitos numéricos.")
        return None
      if not cargo_nome:
        self.mostra_mensagem("Nome do Cargo é obrigatório!")
        return None
      if not telefone or not telefone.isdigit():
        self.mostra_mensagem("Telefone inválido! Deve conter apenas números e não ser vazio.")
        return None
      if not email or "@" not in email or "." not in email:
        self.mostra_mensagem("E-mail inválido! Deve conter '@' e '.'.")
        return None
      
      try:
        salario = float(salario_str.replace(',', '.'))
        if salario < 0:
            raise ValueError
      except ValueError:
        self.mostra_mensagem("Salário inválido! Digite um número positivo.")
        return None
      
      try:
        idade = int(idade_str)
        if idade <= 0 or idade > 120:
            raise ValueError
      except ValueError:
        self.mostra_mensagem("Idade inválida! Digite um número inteiro entre 1 e 120.")
        return None

      # --- INCLUSÃO DOS CAMPOS NO DICIONÁRIO DE RETORNO ---
      return {
          "nome": nome,
          "cpf": cpf,
          "tipo_cargo": cargo_nome,
          "salario": salario,
          "idade": idade,
          "telefone": telefone,
          "email": email
      }
    return None

  def mostra_funcionarios(self, dados_funcionarios: List[Dict[str, Any]]):
    string_todos_funcionarios = "-------- LISTA DE FUNCIONÁRIOS ----------\n\n"
    if not dados_funcionarios:
        string_todos_funcionarios += "Nenhum funcionário cadastrado."
    else:
        for i, dado in enumerate(dados_funcionarios):
            string_todos_funcionarios += f"--- Funcionário {i+1} ---\n"
            string_todos_funcionarios += f"Nome: {dado.get('nome', 'N/A')}\n" # <-- Exibição do nome
            string_todos_funcionarios += f"CPF: {dado.get('cpf', 'N/A')}\n"
            string_todos_funcionarios += f"Cargo: {dado.get('cargo_nome', 'N/A')}\n"
            string_todos_funcionarios += f"Salário: R\${dado.get('salario', 0.0):.2f}\n"
            string_todos_funcionarios += f"Idade: {dado.get('idade', 'N/A')}\n"
            string_todos_funcionarios += f"Telefone: {dado.get('telefone', 'N/A')}\n"
            string_todos_funcionarios += f"E-mail: {dado.get('email', 'N/A')}\n"
            string_todos_funcionarios += "--------------------------------------\n"

    sg.Popup('Lista de Funcionários', string_todos_funcionarios, font=("Helvica", 12))

  def seleciona_funcionario(self) -> Optional[str]:
    sg.ChangeLookAndFeel('DarkBlue3')
    layout = [
      [sg.Text('-------- SELECIONAR FUNCIONÁRIO ----------', font=("Helvica", 20))],
      [sg.Text('Digite o CPF do funcionário:', font=("Helvica", 12))],
      [sg.InputText('', key='cpf_selecionado')], # Campo de entrada para o CPF
      [sg.Button('Confirmar'), sg.Button('Cancelar')]
    ]
    self.__window = sg.Window('Selecionar Funcionário').Layout(layout)

    button, values = self.open()
    self.close()

    if button == 'Confirmar' and values['cpf_selecionado'].strip():
        cpf = values['cpf_selecionado'].strip()
        print(f"DEBUG_TELA: CPF lido na tela para seleção: '{cpf}' (Comprimento: {len(cpf)})")
        if cpf.isdigit() and len(cpf) == 11:
            return cpf
        else:
            self.mostra_mensagem("CPF inválido! Deve conter 11 dígitos numéricos.")
            print(f"DEBUG_TELA: CPF inválido retornado pela tela: '{cpf}'")
            return None
    print(f"DEBUG_TELA: Seleção de funcionário cancelada ou campo vazio na tela.")
    return None

  def confirma_exclusao(self, nome_funcionario: str, cpf_funcionario: str) -> bool:
      """
      Exibe um popup de confirmação de exclusão e retorna True se confirmado, False caso contrário.
      """
      mensagem = f"Tem certeza que deseja excluir o funcionário '{nome_funcionario}' (CPF: {cpf_funcionario})?"
      confirmacao = sg.popup_yes_no(mensagem, title="Confirmar Exclusão", font=("Helvica", 12))
      return confirmacao == 'Yes'

  def mostra_mensagem(self, msg: str):
    """Exibe uma mensagem em um popup do FreeSimpleGUI."""
    sg.popup_ok(msg, font=("Helvica", 12))

  def close(self):
    """Fecha a janela atual do FreeSimpleGUI."""
    if self.__window:
        self.__window.Close()
    self.__window = None

  def open(self):
    """Abre e lê eventos da janela atual do FreeSimpleGUI."""
    if self.__window:
        button, values = self.__window.Read()
        return button, values
    return None, None
