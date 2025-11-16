from telas.tela_abstrata import TelaAbstrata
import FreeSimpleGUI as sg
from typing import Optional, List, Dict, Any
from datetime import datetime

class TelaReserva(TelaAbstrata):
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
        elif values.get('5'):
            opcao = 5
        elif values.get('6'):
            opcao = 6
        elif values.get('7'):
            opcao = 7
        elif values.get('8'):
            opcao = 8
        elif values.get('9'):
            opcao = 9
        elif values.get('0'):
            opcao = 0
    elif button in (None, 'Cancelar'):
        opcao = 0
    
    self.close()
    return opcao

  def init_opcoes(self):
    sg.ChangeLookAndFeel('DarkTeal4')
    layout = [
      [sg.Text('-------- MENU RESERVAS ----------', font=("Helvica", 25))],
      [sg.Text('Escolha sua opção', font=("Helvica", 15))],
      [sg.Radio('Fazer Reserva', "RD1", key='1')],
      [sg.Radio('Listar Reservas', "RD1", key='2')],
      [sg.Radio('Cancelar Reserva', "RD1", key='3')],
      [sg.Radio('Editar Reserva', "RD1", key='4')],
      [sg.Radio('Adicionar Serviço de Quarto a uma Reserva', "RD1", key='5')],
      [sg.Radio('Adicionar Pet a uma Reserva', "RD1", key='6')],
      [sg.Radio('Calcular Valor Total de uma Reserva', "RD1", key='7')],
      [sg.Radio('Relatório por Hóspede', "RD1", key='8')],
      [sg.Radio('Relatório por Tipo de Serviço', "RD1", key='9')],
      [sg.Radio('Retornar', "RD1", key='0', default=True)],
      [sg.Button('Confirmar'), sg.Button('Cancelar')]
    ]
    self.__window = sg.Window('Gerenciar Reservas').Layout(layout)

  def pega_dados_reserva(self, modo: str = "cadastro", dados_atuais: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
    sg.ChangeLookAndFeel('DarkTeal4')
    
    dados_atuais = dados_atuais or {}
    hospedes_val = ", ".join(dados_atuais.get('hospedes_cpfs', []))
    quartos_val = ", ".join(map(str, dados_atuais.get('quartos_ids', [])))
    
    # Tratamento para garantir que dados_atuais.get('checkin') é um objeto datetime/date antes de formatar
    checkin_date_obj = dados_atuais.get('checkin')
    checkin_val = checkin_date_obj.strftime('%d/%m/%Y') if isinstance(checkin_date_obj, (datetime, datetime.date)) else ''
    
    checkout_date_obj = dados_atuais.get('checkout')
    checkout_val = checkout_date_obj.strftime('%d/%m/%Y') if isinstance(checkout_date_obj, (datetime, datetime.date)) else ''

    layout = [
      [sg.Text(f'-------- DADOS DA RESERVA ({modo.upper()}) ----------', font=("Helvica", 25))],
      [sg.Text('CPFs do(s) Hóspede(s) (separados por vírgula):', size=(30, 1)), sg.InputText(hospedes_val, key='hospedes_cpfs')],
      [sg.Text('Numero do(s) Quarto(s) (separados por vírgula):', size=(30, 1)), sg.InputText(quartos_val, key='quartos_ids')],
      [sg.Text('Data Check-in (DD/MM/AAAA):', size=(30, 1)), sg.InputText(checkin_val, key='checkin_data')],
      [sg.Text('Data Check-out (DD/MM/AAAA):', size=(30, 1)), sg.InputText(checkout_val, key='checkout_data')],
      [sg.Button('Confirmar'), sg.Button('Cancelar')]
    ]
    self.__window = sg.Window('Dados da Reserva').Layout(layout)

    button, values = self.open()
    self.close()

    if button == 'Confirmar':
      hospedes_cpfs_str = values['hospedes_cpfs'].strip()
      quartos_ids_str = values['quartos_ids'].strip()
      checkin_data_str = values['checkin_data'].strip()
      checkout_data_str = values['checkout_data'].strip()

      if not hospedes_cpfs_str:
        self.mostra_mensagem("Pelo menos um CPF de hóspede é obrigatório!")
        return None
      if not quartos_ids_str:
        self.mostra_mensagem("Pelo menos um ID de quarto é obrigatório!")
        return None
      if not checkin_data_str:
        self.mostra_mensagem("Data de Check-in é obrigatória!")
        return None
      if not checkout_data_str:
        self.mostra_mensagem("Data de Check-out é obrigatória!")
        return None

      hospedes_cpfs = [cpf.strip() for cpf in hospedes_cpfs_str.split(',') if cpf.strip()]
      if not hospedes_cpfs:
          self.mostra_mensagem("Pelo menos um CPF de hóspede válido é obrigatório!")
          return None
      for cpf in hospedes_cpfs:
          if not cpf.isdigit() or len(cpf) != 11:
              self.mostra_mensagem(f"CPF '{cpf}' inválido! Deve conter 11 dígitos numéricos.")
              return None

      try:
          quartos_ids = [int(q_id.strip()) for q_id in quartos_ids_str.split(',') if q_id.strip()]
          if not quartos_ids:
              self.mostra_mensagem("Pelo menos um ID de quarto válido é obrigatório!")
              return None
      except ValueError:
          self.mostra_mensagem("IDs de quarto inválidos! Digite apenas números separados por vírgula.")
          return None

      try:
        checkin_data = datetime.strptime(checkin_data_str, '%d/%m/%Y').date()
        checkout_data = datetime.strptime(checkout_data_str, '%d/%m/%Y').date()
        if checkout_data <= checkin_data:
          self.mostra_mensagem("Data de Check-out deve ser posterior à data de Check-in.")
          return None
      except ValueError:
        self.mostra_mensagem("Formato de data inválido. Use DD/MM/AAAA.")
        return None

      return {
          "hospedes_cpfs": hospedes_cpfs,
          "quartos_ids": quartos_ids,
          "checkin_data": checkin_data,
          "checkout_data": checkout_data,
      }
    return None # Se Cancelar ou fechar a janela

  def mostra_reservas(self, dados_reservas: List[Dict[str, Any]]):
    string_todas_reservas = "------------ LISTA DE RESERVAS --------------\n\n"
    if not dados_reservas:
        string_todas_reservas += "Nenhuma reserva cadastrada."
    else:
        for i, dado in enumerate(dados_reservas):
            # CORREÇÃO: Acessar a lista 'hospedes' e extrair o 'nome' de cada dicionário de hóspede
            hospedes_nomes = ", ".join([hospede.get('nome', 'N/A') for hospede in dado.get('hospedes', [])])
            # CORREÇÃO: Acessar a lista 'quartos' e extrair o 'numero' de cada dicionário de quarto
            quartos_str = ", ".join([str(quarto.get('numero', 'N/A')) for quarto in dado.get('quartos', [])])

            string_todas_reservas += f"Reserva ID: {dado.get('id', 'N/A')} | Hóspedes: {hospedes_nomes} | Quartos: {quartos_str} | " \
                                   f"Check-in: {dado.get('checkin', 'N/A')} | Check-out: {dado.get('checkout', 'N/A')} | " \
                                   f"Status: {dado.get('status', 'N/A')} | Valor Total: R$ {dado.get('valor_total', 0.0):.2f}\n"

            if dado.get('servicos_quarto'):
                string_todas_reservas += "  Serviços de Quarto:\n"
                for servico in dado['servicos_quarto']:
                    # CORREÇÃO: Usar as chaves corretas 'tipo_servico' e 'quarto_numero'
                    string_todas_reservas += f"    - Tipo: {servico.get('tipo_servico', 'N/A')}, Valor: R$ {servico.get('valor', 0.0):.2f}, Quarto: {servico.get('quarto_numero', 'N/A')}, Funcionário: {servico.get('funcionario_nome', 'N/A')}\n"
            
            if dado.get('pets'):
                string_todas_reservas += "  Pets:\n"
                for pet in dado['pets']:
                    string_todas_reservas += f"    - Nome: {pet.get('nome_pet', 'N/A')}, Espécie: {pet.get('especie', 'N/A')}\n"
            string_todas_reservas += "----------------------------------------------------------\n"

    sg.Popup('Lista de Reservas', string_todas_reservas, font=("Helvica", 12))

  def seleciona_reserva(self) -> Optional[str]:
    sg.ChangeLookAndFeel('DarkTeal4')
    layout = [
      [sg.Text('-------- SELECIONAR RESERVA ----------', font=("Helvica", 20))],
      [sg.Text('Digite o ID da reserva ou parte do nome do hóspede principal:', font=("Helvica", 12))],
      [sg.InputText('', key='identificador_reserva')],
      [sg.Button('Confirmar'), sg.Button('Cancelar')]
    ]
    self.__window = sg.Window('Selecionar Reserva').Layout(layout)

    button, values = self.open()
    self.close()

    if button == 'Confirmar' and values['identificador_reserva'].strip():
        identificador = values['identificador_reserva'].strip()
        return identificador
    return None

  def confirma_cancelamento(self, id_reserva: int, hospedes_nomes: str) -> bool:
      mensagem = f"Tem certeza que deseja cancelar a Reserva ID {id_reserva} (Hóspedes: {hospedes_nomes})?"
      confirmacao = sg.popup_yes_no(mensagem, title="Confirmar Cancelamento", font=("Helvica", 12))
      return confirmacao == 'Yes'

  def confirma_edicao(self, id_reserva: int, hospedes_nomes: str) -> bool:
      mensagem = f"Tem certeza que deseja editar a Reserva ID {id_reserva} (Hóspedes: {hospedes_nomes})?"
      confirmacao = sg.popup_yes_no(mensagem, title="Confirmar Edição", font=("Helvica", 12))
      return confirmacao == 'Yes'

  def pega_dados_servico_quarto(self) -> Optional[Dict[str, Any]]:
    sg.ChangeLookAndFeel('DarkTeal4')
    layout = [
      [sg.Text('-------- DADOS DO SERVIÇO DE QUARTO ----------', font=("Helvica", 25))],
      [sg.Text('Tipo de serviço:', size=(28, 1)), sg.InputText('', key='tipo_servico')],
      [sg.Text('Valor do serviço (ex: 25.00):', size=(28, 1)), sg.InputText('', key='valor_servico')],
      [sg.Text('Número do quarto (da reserva):', size=(28, 1)), sg.InputText('', key='num_quarto')],
      [sg.Text('CPF do funcionário responsável:', size=(28, 1)), sg.InputText('', key='cpf_funcionario')],
      [sg.Button('Confirmar'), sg.Button('Cancelar')]
    ]
    self.__window = sg.Window('Dados Serviço de Quarto').Layout(layout)

    button, values = self.open()
    self.close()

    if button == 'Confirmar':
      tipo_servico = values['tipo_servico'].strip()
      valor_str = values['valor_servico'].strip()
      num_quarto_str = values['num_quarto'].strip()
      cpf_funcionario = values['cpf_funcionario'].strip()

      if not tipo_servico:
        self.mostra_mensagem("Tipo de serviço é obrigatório!")
        return None
      
      try:
        valor = float(valor_str.replace(',', '.')) 
        if valor <= 0:
            self.mostra_mensagem("Valor do serviço inválido! Deve ser um número positivo.")
            return None
      except ValueError:
        self.mostra_mensagem("Valor inválido! Por favor, digite um número (ex: 25.00).")
        return None
      
      try:
          num_quarto = int(num_quarto_str)
          if num_quarto <= 0:
              self.mostra_mensagem("Número do quarto inválido! Deve ser um número inteiro positivo.")
              return None
      except ValueError:
          self.mostra_mensagem("Número do quarto inválido! Digite um número inteiro.")
          return None
      
      if not cpf_funcionario or not cpf_funcionario.isdigit() or len(cpf_funcionario) != 11:
        self.mostra_mensagem("CPF do funcionário inválido! Deve conter 11 dígitos numéricos.")
        return None

      return {
          "tipo_servico": tipo_servico,
          "valor": valor,
          "num_quarto": num_quarto,
          "cpf_funcionario": cpf_funcionario
      }
    return None # Se Cancelar ou fechar a janela
  
  def pega_dados_pet(self) -> Optional[Dict[str, Any]]:
          sg.ChangeLookAndFeel('DarkTeal4')
          layout = [
            [sg.Text('-------- ADICIONAR PET ----------', font=("Helvica", 20))],
            [sg.Text('Nome do Pet:', size=(20, 1)), sg.InputText('', key='nome_pet')],
            [sg.Text('Espécie do Pet (Ex: Cachorro, Gato):', size=(20, 1)), sg.InputText('', key='especie')], 
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
          ]
          self.__window = sg.Window('Adicionar Pet').Layout(layout)

          button, values = self.open()
          self.close()  

          if button == 'Confirmar':
            nome_pet = values['nome_pet'].strip()
            especie_pet = values['especie'].strip()

            if not nome_pet:
              self.mostra_mensagem("Nome do pet é obrigatório!")
              return None
            if not especie_pet:
              self.mostra_mensagem("Espécie do pet é obrigatória!")
              return None
            
            return {
                "nome_pet": nome_pet,
                "especie": especie_pet
            }
          return None
    
  def mostra_valor_total(self, id_reserva: int, valor_total: float):
      sg.Popup(f"Reserva ID {id_reserva}", f"O valor total da reserva é: R$ {valor_total:.2f}", font=("Helvica", 12))

  def pega_cpf_hospede_relatorio(self) -> Optional[str]:
      sg.ChangeLookAndFeel('DarkTeal4')
      layout = [
          [sg.Text('-------- RELATÓRIO POR HÓSPEDE ----------', font=("Helvica", 20))],
          [sg.Text('Digite o CPF do hóspede para o relatório:', font=("Helvica", 12))],
          [sg.InputText('', key='cpf_hospede')],
          [sg.Button('Confirmar'), sg.Button('Cancelar')]
      ]
      self.__window = sg.Window('Relatório por Hóspede').Layout(layout)

      button, values = self.open()
      self.close()

      if button == 'Confirmar' and values['cpf_hospede'].strip():
          cpf = values['cpf_hospede'].strip()
          if cpf.isdigit() and len(cpf) == 11:
              return cpf
          else:
              self.mostra_mensagem("CPF inválido! Deve conter 11 dígitos numéricos.")
              return None
      return None
  
  def mostra_relatorio_hospede(self, cpf_hospede: str, dados_reservas: List[Dict[str, Any]]):
      string_relatorio = f"--- RELATÓRIO DE RESERVAS PARA HÓSPEDE CPF: {cpf_hospede} ---\n\n"
      if not dados_reservas:
          string_relatorio += "Nenhuma reserva encontrada para este hóspede."
      else:
          for i, dado in enumerate(dados_reservas):
              # CORREÇÃO: Acessar a lista 'hospedes' e extrair o 'nome' de cada dicionário de hóspede
              hospedes_nomes = ", ".join([hospede.get('nome', 'N/A') for hospede in dado.get('hospedes', [])])
              # CORREÇÃO: Acessar a lista 'quartos' e extrair o 'numero' de cada dicionário de quarto
              quartos_str = ", ".join([str(quarto.get('numero', 'N/A')) for quarto in dado.get('quartos', [])])
              
              string_relatorio += f"--- Reserva ID: {dado.get('id', 'N/A')} ---\n"
              string_relatorio += f"  Hóspedes: {hospedes_nomes}\n"
              string_relatorio += f"  Quartos: {quartos_str}\n"
              string_relatorio += f"  Check-in: {dado.get('checkin', 'N/A')}\n"
              string_relatorio += f"  Check-out: {dado.get('checkout', 'N/A')}\n"
              string_relatorio += f"  Status: {dado.get('status', 'N/A')}\n"
              string_relatorio += f"  Valor Total: R$ {dado.get('valor_total', 0.0):.2f}\n"
              if dado.get('servicos_quarto'):
                  string_relatorio += "    Serviços de Quarto:\n"
                  for servico in dado['servicos_quarto']:
                      # CORREÇÃO: Usar as chaves corretas 'tipo_servico' e 'quarto_numero'
                      string_relatorio += f"      - Tipo: {servico.get('tipo_servico', 'N/A')}, Valor: R$ {servico.get('valor', 0.0):.2f}, Quarto: {servico.get('quarto_numero', 'N/A')}\n"
              string_relatorio += "--------------------------------------\n"
      sg.Popup('Relatório por Hóspede', string_relatorio, font=("Helvica", 12))

  def pega_tipo_servico_relatorio(self) -> Optional[str]:
      sg.ChangeLookAndFeel('DarkTeal4')
      layout = [
          [sg.Text('-------- RELATÓRIO POR TIPO DE SERVIÇO ----------', font=("Helvica", 20))],
          [sg.Text('Digite o tipo de serviço para o relatório:', font=("Helvica", 12))],
          [sg.InputText('', key='tipo_servico')],
          [sg.Button('Confirmar'), sg.Button('Cancelar')]
      ]
      self.__window = sg.Window('Relatório por Tipo de Serviço').Layout(layout)

      button, values = self.open()
      self.close()

      if button == 'Confirmar' and values['tipo_servico'].strip():
          return values['tipo_servico'].strip()
      return None

  def mostra_relatorio_servico(self, tipo_servico: str, dados_servicos: List[Dict[str, Any]]):
      string_relatorio = f"-------- RELATÓRIO DE SERVIÇOS TIPO: {tipo_servico.upper()} ----------\n\n"
      if not dados_servicos:
          string_relatorio += "Nenhum serviço deste tipo encontrado."
      else:
          for i, servico in enumerate(dados_servicos):
              # Essas chaves estão corretas, pois o ControladorReserva constrói o dicionário para este relatório
              string_relatorio += f"--- Serviço {i+1} ---\n"
              string_relatorio += f"  Reserva ID: {servico.get('reserva_id', 'N/A')}\n"
              string_relatorio += f"  Tipo: {servico.get('tipo', 'N/A')}\n"
              string_relatorio += f"  Valor: R$ {servico.get('valor', 0.0):.2f}\n"
              string_relatorio += f"  Quarto: {servico.get('num_quarto', 'N/A')}\n"
              string_relatorio += f"  Funcionário: {servico.get('funcionario_nome', 'N/A')} (CPF: {servico.get('funcionario_cpf', 'N/A')})\n"
              string_relatorio += "--------------------------------------\n"
      sg.Popup('Relatório por Tipo de Serviço', string_relatorio, font=("Helvica", 12))

  def mostra_mensagem(self, msg: str):
    sg.popup_ok(msg, font=("Helvica", 12))

  def close(self):
    if self.__window:
        self.__window.Close()
    self.__window = None

  def open(self):
    if self.__window:
        button, values = self.__window.Read()
        return button, values
    return None, None