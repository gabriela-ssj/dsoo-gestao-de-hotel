from entidades.hotel import Hotel
from entidades.hospede import Hospede
from entidades.quarto import Quarto
from entidades.reserva import Reserva
from telas.tela_hotel import TelaHotel
from collections import Counter

class ControladorHotel:
    def __init__(self, hotel: Hotel, controlador_sistema):
        self.__hotel = hotel
        self.__tela = TelaHotel()
        self.__controlador_sistema = controlador_sistema

    def incluir_hospede(self):
        dados = self.__tela.pega_dados_hospede()
        hospede = Hospede(**dados)
        self.__hotel.adicionar_hospede(hospede)

    def alterar_hospede(self):
        cpf = self.__tela.seleciona_hospede()
        novos_dados = self.__tela.pega_dados_hospede()
        for h in self.__hotel.hospedes:
            if h.cpf == cpf:
                h.nome = novos_dados["nome"]
                h.idade = novos_dados["idade"]
                h.telefone = novos_dados["telefone"]
                h.email = novos_dados["email"]
                self.__tela.mostra_mensagem("✅ Hóspede alterado.")
                return
        self.__tela.mostra_mensagem("⚠️ Hóspede não encontrado.")

    def listar_hospedes(self):
        lista = self.__hotel.listar_hospedes()
        self.__tela.mostra_lista(lista)

    def excluir_hospede(self):
        cpf = self.__tela.seleciona_hospede()
        self.__hotel.excluir_hospede(cpf)

    def incluir_quarto(self):
        dados = self.__tela.pega_dados_quarto()
        tipo = dados.pop("tipo")
        if tipo == "suite":
            from entidades.quarto import Suite
            quarto = Suite(**dados)
        elif tipo == "duplo":
            from entidades.quarto import Duplo
            quarto = Duplo(**dados)
        elif tipo == "simples":
            from entidades.quarto import Simples
            quarto = Simples(**dados)
        else:
            self.__tela.mostra_mensagem("⚠️ Tipo de quarto inválido.")
            return
        self.__hotel.adicionar_quarto(quarto)

    def alterar_quarto(self):
        numero = self.__tela.seleciona_quarto()
        novos_dados = self.__tela.pega_dados_quarto()
        self.__hotel.alterar_quarto(numero, novos_dados)

    def listar_quartos(self):
        lista = self.__hotel.listar_quartos()
        self.__tela.mostra_lista(lista)

    def excluir_quarto(self):
        numero = self.__tela.seleciona_quarto()
        self.__hotel.excluir_quarto(numero)

    def incluir_reserva(self):
        dados = self.__tela.pega_dados_reserva()
        reserva = Reserva([], [], dados["checkin"], dados["checkout"], "pendente")
        self.__hotel.adicionar_reserva(reserva)

    def listar_reservas(self):
        lista = self.__hotel.listar_reservas()
        self.__tela.mostra_lista(lista)

    def relatorio_quartos_mais_reservados(self):
        total_reservas = len(self.__hotel._Hotel__reservas)
        contador = Counter()
        for reserva in self.__hotel._Hotel__reservas:
            for quarto in reserva.quartos:
                contador[quarto.numero] += 1
        relatorio = []
        for numero, total in contador.items():
            porcentagem = (total / total_reservas) * 100 if total_reservas else 0
            relatorio.append(f"Quarto {numero}: {total} reservas ({porcentagem:.1f}%)")
        self.__tela.mostra_lista(relatorio)

    def retornar(self):
        self.__controlador_sistema.abre_tela()

    def abre_tela(self):
        opcoes = {
            1: self.incluir_hospede,
            2: self.alterar_hospede,
            3: self.listar_hospedes,
            4: self.excluir_hospede,
            5: self.incluir_quarto,
            6: self.alterar_quarto,
            7: self.listar_quartos,
            8: self.excluir_quarto,
            9: self.incluir_reserva,
            10: self.listar_reservas,
            11: self.relatorio_quartos_mais_reservados,
            0: self.retornar
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
            else:
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")
