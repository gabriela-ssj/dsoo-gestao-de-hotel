from telas.tela_abstrata import TelaAbstrata
import FreeSimpleGUI as sg
from typing import Optional, List, Dict, Any
from datetime import datetime, date

class TelaReserva(TelaAbstrata):
    def __init__(self):
        self.__window = None

    def _parse_data(self, s: str) -> Optional[date]:
        try:
            return datetime.strptime(s.strip(), "%d/%m/%Y").date()
        except Exception:
            return None


    def tela_opcoes(self) -> int:
        self.init_opcoes()
        button, values = self.open()
        
        opcao = 0
        if button == 'Confirmar':
            for num in [1,2,3,4,5,6,7,8,9,0]:
                if values.get(str(num)):
                    opcao = num
                    break

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
            [sg.Radio('Adicionar Serviço de Quarto', "RD1", key='5')],
            [sg.Radio('Adicionar Pet', "RD1", key='6')],
            [sg.Radio('Calcular Valor Total', "RD1", key='7')],
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

        checkin_val = ""
        if "checkin" in dados_atuais and isinstance(dados_atuais["checkin"], (datetime, date)):
            checkin_val = dados_atuais["checkin"].strftime('%d/%m/%Y')

        checkout_val = ""
        if "checkout" in dados_atuais and isinstance(dados_atuais["checkout"], (datetime, date)):
            checkout_val = dados_atuais["checkout"].strftime('%d/%m/%Y')

        layout = [
            [sg.Text(f'-------- DADOS DA RESERVA ({modo.upper()}) ----------', font=("Helvica", 25))],
            [sg.Text('CPFs dos Hóspedes (separados por vírgula):'), sg.InputText(hospedes_val, key='hospedes_cpfs')],
            [sg.Text('Número dos Quarto(s) (separados por vírgula):'), sg.InputText(quartos_val, key='quartos_ids')],
            [sg.Text('Data Check-in (DD/MM/AAAA):'), sg.InputText(checkin_val, key='checkin_data')],
            [sg.Text('Data Check-out (DD/MM/AAAA):'), sg.InputText(checkout_val, key='checkout_data')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        self.__window = sg.Window('Dados da Reserva').Layout(layout)

        button, values = self.open()
        self.close()

        if button != 'Confirmar':
            return None

        hospedes_cpfs = [c.strip() for c in values['hospedes_cpfs'].split(',') if c.strip()]
        if not hospedes_cpfs:
            self.mostra_mensagem("Digite pelo menos um CPF.")
            return None

        for cpf in hospedes_cpfs:
            if not cpf.isdigit() or len(cpf) != 11:
                self.mostra_mensagem(f"CPF inválido: {cpf}")
                return None

        try:
            quartos_ids = [int(x.strip()) for x in values['quartos_ids'].split(',') if x.strip()]
        except:
            self.mostra_mensagem("IDs de quartos inválidos!")
            return None

        if not quartos_ids:
            self.mostra_mensagem("Digite pelo menos um quarto.")
            return None

        checkin_data = self._parse_data(values['checkin_data'])
        checkout_data = self._parse_data(values['checkout_data'])

        if not checkin_data:
            self.mostra_mensagem("Data de Check-in inválida.")
            return None

        if not checkout_data:
            self.mostra_mensagem("Data de Check-out inválida.")
            return None

        if checkout_data <= checkin_data:
            self.mostra_mensagem("Check-out deve ser depois do Check-in.")
            return None

        return {
            "hospedes_cpfs": hospedes_cpfs,
            "quartos_ids": quartos_ids,
            "checkin_data": checkin_data,
            "checkout_data": checkout_data
        }

    def mostra_reservas(self, reservas: List[Dict[str, Any]]):
        texto = "------------ LISTA DE RESERVAS --------------\n\n"

        if not reservas:
            texto += "Nenhuma reserva cadastrada."
        else:
            for r in reservas:
                hospedes = ", ".join([h.get("nome", "N/A") for h in r.get("hospedes", [])])
                quartos = ", ".join([str(q.get("numero", "N/A")) for q in r.get("quartos", [])])

                texto += (
                    f"Reserva ID: {r.get('id')}\n"
                    f"  Hóspedes: {hospedes}\n"
                    f"  Quartos: {quartos}\n"
                    f"  Check-in: {r.get('checkin')}\n"
                    f"  Check-out: {r.get('checkout')}\n"
                    f"  Status: {r.get('status')}\n"
                    f"  Valor Total: R$ {r.get('valor_total', 0.0):.2f}\n"
                    f"----------------------------------------------------------\n"
                )

        sg.Popup('Lista de Reservas', texto, font=("Helvica", 12))


    def seleciona_reserva(self) -> Optional[str]:
        sg.ChangeLookAndFeel('DarkTeal4')
        layout = [
            [sg.Text('-------- SELECIONAR RESERVA ----------', font=("Helvica", 20))],
            [sg.InputText('', key='ident')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        
        self.__window = sg.Window('Selecionar Reserva').Layout(layout)
        button, values = self.open()
        self.close()

        if button == 'Confirmar' and values['ident'].strip():
            return values['ident'].strip()
        return None

    def confirma_cancelamento(self, id_reserva: int, hospedes_nomes: str) -> bool:
        return sg.popup_yes_no(
            f"Deseja cancelar a reserva {id_reserva} ({hospedes_nomes})?"
        ) == "Yes"

    def confirma_edicao(self, id_reserva: int, hospedes_nomes: str) -> bool:
        return sg.popup_yes_no(
            f"Deseja editar a reserva {id_reserva} ({hospedes_nomes})?"
        ) == "Yes"

    def pega_dados_servico_quarto(self):
        sg.ChangeLookAndFeel('DarkTeal4')
        layout = [
            [sg.Text('-------- SERVIÇO DE QUARTO ----------')],
            [sg.Text('Tipo:'), sg.InputText('', key='tipo')],
            [sg.Text('Valor:'), sg.InputText('', key='valor')],
            [sg.Text('Número do quarto:'), sg.InputText('', key='num')],
            [sg.Text('CPF funcionário:'), sg.InputText('', key='cpf')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        
        self.__window = sg.Window('Serviço Quarto').Layout(layout)
        button, values = self.open()
        self.close()

        if button != "Confirmar":
            return None

        try:
            valor = float(values['valor'].replace(",", "."))
        except:
            self.mostra_mensagem("Valor inválido!")
            return None

        return {
            "tipo_servico": values["tipo"],
            "valor": valor,
            "num_quarto": int(values["num"]),
            "cpf_funcionario": values["cpf"]
        }

    def pega_dados_pet(self):
        sg.ChangeLookAndFeel('DarkTeal4')
        layout = [
            [sg.Text('-------- ADICIONAR PET ----------')],
            [sg.Text('Nome:'), sg.InputText('', key='nome')],
            [sg.Text('Espécie:'), sg.InputText('', key='especie')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        self.__window = sg.Window('Pet').Layout(layout)
        button, values = self.open()
        self.close()

        if button != "Confirmar":
            return None

        return {"nome_pet": values['nome'], "especie": values['especie']}

    def pega_cpf_hospede_relatorio(self) -> Optional[str]:
        sg.ChangeLookAndFeel('DarkTeal4')
        layout = [
            [sg.Text('CPF do hóspede:')],
            [sg.InputText('', key='cpf')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]
        
        self.__window = sg.Window('Relatório Hóspede').Layout(layout)
        button, values = self.open()
        self.close()

        cpf = values["cpf"].strip()
        if button == "Confirmar" and cpf.isdigit() and len(cpf) == 11:
            return cpf

        return None

    def mostra_relatorio_hospede(self, cpf: str, reservas: List[Dict[str, Any]]):
        texto = f"--- RELATÓRIO DO HÓSPEDE {cpf} ---\n\n"
        for r in reservas:
            texto += f"Reserva {r['id']} - Total: R$ {r['valor_total']:.2f}\n"
        sg.Popup("Relatório", texto)

    def pega_tipo_servico_relatorio(self) -> Optional[str]:
        sg.ChangeLookAndFeel('DarkTeal4')
        layout = [
            [sg.Text('Tipo do serviço:')],
            [sg.InputText('', key='tipo')],
            [sg.Button('Confirmar'), sg.Button('Cancelar')]
        ]

        self.__window = sg.Window('Relatório Serviço').Layout(layout)
        button, v = self.open()
        self.close()

        if button == "Confirmar" and v["tipo"].strip():
            return v["tipo"].strip()
        return None

    def mostra_relatorio_servico(self, tipo_servico: str, servicos: List[Dict[str, Any]]):
        texto = f"--- SERVIÇOS DO TIPO {tipo_servico.upper()} ---\n"
        for s in servicos:
            texto += f"{s}\n"
        sg.Popup("Relatório Serviço", texto)


    def mostra_mensagem(self, msg: str):
        sg.popup_ok(msg)

    def close(self):
        if self.__window:
            self.__window.Close()
            self.__window = None

    def open(self):
        if self.__window:
            return self.__window.Read()
        return None, None
