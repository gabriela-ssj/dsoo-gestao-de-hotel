from entidades.quarto import Quarto
from entidades.quartos import Suite, Duplo, Simples
from telas.tela_quarto import TelaQuarto
from controlers.controlador_hotel import ControladorHotel

class ControladorQuarto:
    def __init__(self):
        self.__quartos: list[Quarto] = []
        self.__tela = TelaQuarto()

    def abre_tela(self):
        opcoes = {
            1: self.cadastrar_quarto,
            2: self.listar_quartos,
            3: self.alterar_quarto,
            4: self.excluir_quarto,
            0: self.retornar
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
                if opcao == 0:
                    break
            else:
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")

    def retornar(self):
        ControladorHotel().abre_tela()

    def cadastrar_quarto(self):
        dados = self.__tela.pega_dados_quarto()
        tipo = dados["tipo"]
        numero_base = dados["numero"]

        if tipo == "suite":
            numero_formatado = f"S{numero_base}"
            if self.buscar_quarto(numero_formatado):
                self.__tela.mostra_mensagem(f"⚠️ Quarto {numero_formatado} já está cadastrado.")
                return
            quarto = Suite(numero_base, dados["valor_diaria"], dados["disponibilidade"], dados["hidro"])

        elif tipo == "duplo":
            numero_formatado = f"D{numero_base}"
            if self.buscar_quarto(numero_formatado):
                self.__tela.mostra_mensagem(f"⚠️ Quarto {numero_formatado} já está cadastrado.")
                return
            quarto = Duplo(numero_base, dados["valor_diaria"], dados["disponibilidade"])

        elif tipo == "simples":
            numero_formatado = f"Q{numero_base}"
            if self.buscar_quarto(numero_formatado):
                self.__tela.mostra_mensagem(f"⚠️ Quarto {numero_formatado} já está cadastrado.")
                return
            quarto = Simples(numero_base, dados["valor_diaria"], dados["disponibilidade"])

        else:
            self.__tela.mostra_mensagem("⚠️ Tipo de quarto inválido.")
            return

        self.__quartos.append(quarto)
        self.__tela.mostra_mensagem(f"✅ Quarto {quarto.numero} cadastrado com sucesso.")

    def listar_quartos(self):
        if not self.__quartos:
            self.__tela.mostra_mensagem("Nenhum quarto cadastrado.")
            return
        lista = []
        for q in self.__quartos:
            tipo = type(q).__name__
            status = "Disponível" if q.disponibilidade else "Ocupado"
            lista.append(f"{tipo} nº {q.numero} | Diária: R${q.valor_diaria:.2f} | {status}")
        self.__tela.mostra_lista(lista)

    def alterar_quarto(self):
        numero = self.__tela.seleciona_quarto()
        quarto = self.buscar_quarto(numero)
        if not quarto:
            self.__tela.mostra_mensagem(f"⚠️ Quarto {numero} não encontrado.")
            return

        dados = self.__tela.pega_dados_quarto()
        quarto.valor_diaria = dados["valor_diaria"]
        quarto.disponibilidade = dados["disponibilidade"]

        if isinstance(quarto, Suite):
            quarto.hidro = dados["hidro"]

        self.__tela.mostra_mensagem(f"✅ Quarto {quarto.numero} alterado com sucesso.")

    def excluir_quarto(self):
        numero = self.__tela.seleciona_quarto()
        quarto = self.buscar_quarto(numero)
        if quarto:
            self.__quartos.remove(quarto)
            self.__tela.mostra_mensagem(f"✅ Quarto {numero} excluído.")
        else:
            self.__tela.mostra_mensagem(f"⚠️ Quarto {numero} não encontrado.")

    def buscar_quarto(self, numero: str):
        for q in self.__quartos:
            if q.numero == numero:
                return q
        return None
