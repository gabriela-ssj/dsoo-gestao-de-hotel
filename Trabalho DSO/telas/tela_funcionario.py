from telas.tela_abstrata import TelaAbstrata
import FreeSimpleGUI as sg
from typing import Optional, List, Dict, Any
import re 

class TelaFuncionario(TelaAbstrata):
  def __init__(self):
    self.__window = None

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

    self.close()
    return opcao_selecionada

  def init_opcoes(self):
    """
    Define o layout da janela principal de opções do menu de funcionários.
    """
    sg.ChangeLookAndFeel('DarkBlue3')
    layout = [
      [sg.Text('-------- FUNCIONÁRIOS ----------', font=("Helvica", 25))],
      [sg.Text('Escolha sua opção', font=("Helvica", 15))],
      [sg.Radio('Cadastrar Funcionário', "RD1", key='1', enable_events=True)], 
      [sg.Radio('Listar Funcionários', "RD1", key='2', enable_events=True)],
      [sg.Radio('Alterar Funcionário', "RD1", key='3', enable_events=True)],
      [sg.Radio('Excluir Funcionário', "RD1", key='4', enable_events=True)],
      [sg.Radio('Retornar', "RD1", key='0', default=True, enable_events=True)],
      [sg.Button('Confirmar'), sg.Button('Cancelar')]
    ]
    self.__window = sg.Window('Gerenciar Funcionários').Layout(layout)

  def pega_dados_funcionario(self, modo: str = "cadastro", dados_atuais: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:

    sg.ChangeLookAndFeel('DarkTeal4')

    dados_atuais = dados_atuais or {}
    cpf_val = dados_atuais.get('cpf', '')
    nome_val = dados_atuais.get('nome', '')
    cargo_nome_val = dados_atuais.get('tipo_cargo', dados_atuais.get('cargo_nome', '')) 
    salario_val = str(dados_atuais.get('salario', ''))
    idade_val = str(dados_atuais.get('idade', ''))
    telefone_val = dados_atuais.get('telefone', '')
    email_val = dados_atuais.get('email', '')

    layout = [
      [sg.Text(f'-------- DADOS FUNCIONÁRIO ({modo.upper()}) ----------', font=("Helvica", 25))],
      [sg.Text('Nome:', size=(15, 1)), sg.InputText(nome_val, key='nome')], 
      [sg.Text('CPF (11 dígitos):', size=(15, 1)), sg.InputText(cpf_val, key='cpf', disabled=(modo == "alteracao"))], 
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
      if not all(c.isalpha() or c.isspace() for c in nome): 
          self.mostra_mensagem("⚠️ O nome deve conter apenas letras.")
          return None

      if modo == "cadastro":
        if not cpf or not cpf.isdigit() or len(cpf) != 11:
          self.mostra_mensagem("CPF inválido! Deve conter 11 dígitos numéricos.")
          return None
      
      if not cargo_nome:
        self.mostra_mensagem("Nome do Cargo é obrigatório!")
        return None
      
      if not telefone.isdigit() or not (8 <= len(telefone) <= 15):
        self.mostra_mensagem("Telefone inválido! Use apenas números (8 a 15 dígitos).")
        return None
      
      padrao_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
      if not re.match(padrao_email, email):
        self.mostra_mensagem("E-mail inválido! Exemplo válido: nome@dominio.com")
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
        if idade < 16 or idade > 120:
            self.mostra_mensagem("Idade inválida! Digite um número inteiro entre 16 e 120.")
            return None
      except ValueError:
        self.mostra_mensagem("Idade inválida! Digite um número inteiro.")
        return None

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
    """
    Exibe uma lista de funcionários em um popup do FreeSimpleGUI.
    :param dados_funcionarios: Lista de dicionários, cada um representando um funcionário.
    """
    string_todos_funcionarios = "-------- LISTA DE FUNCIONÁRIOS ----------\n\n"
    if not dados_funcionarios:
        string_todos_funcionarios += "Nenhum funcionário cadastrado."
    else:
        for i, dado in enumerate(dados_funcionarios):
            string_todos_funcionarios += f"--- Funcionário {i+1} ---\n"
            string_todos_funcionarios += f"Nome: {dado.get('nome', 'N/A')}\n"
            string_todos_funcionarios += f"CPF: {dado.get('cpf', 'N/A')}\n"
            string_todos_funcionarios += f"Cargo: {dado.get('tipo_cargo', 'N/A')}\n"
            string_todos_funcionarios += f"Salário: R\${dado.get('salario', 0.0):.2f}\n"
            string_todos_funcionarios += f"Idade: {dado.get('idade', 'N/A')}\n"
            string_todos_funcionarios += f"Telefone: {dado.get('telefone', 'N/A')}\n"
            string_todos_funcionarios += f"E-mail: {dado.get('email', 'N/A')}\n"
            string_todos_funcionarios += "--------------------------------------\n"

    sg.Popup('Lista de Funcionários', string_todos_funcionarios, font=("Helvica", 12))

  def seleciona_funcionario(self) -> Optional[str]:
    """
    Solicita ao usuário o CPF de um funcionário.
    :return: O CPF do funcionário (string) ou None se a operação for cancelada.
    """
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
        if cpf.isdigit() and len(cpf) == 11:
            return cpf
        else:
            self.mostra_mensagem("CPF inválido! Deve conter 11 dígitos numéricos.")
            return None
    return None

  def confirma_acao(self, mensagem: str) -> bool:
      """
      Exibe um popup de confirmação de ação e retorna True se confirmado, False caso contrário.
      """
      confirmacao = sg.popup_yes_no(mensagem, title="Confirmar Ação", font=("Helvica", 12))
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
