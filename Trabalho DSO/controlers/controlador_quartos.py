from entidades.quartos import Suite, Duplo, Simples
from entidades.quarto import Quarto
from telas.tela_quarto import TelaQuarto
from controlers.ValidacaoException import ValidacaoException


class ControladorQuarto:
    def __init__(self):
        self.__quartos: list[Quarto] = []
        self.__tela = TelaQuarto()

        self.__mapa_tipos = {
            "suite": Suite,
            "duplo": Duplo,
            "simples": Simples
        }

        self.__valores_diaria = {
            "suite": 300.0,
            "duplo": 200.0,
            "simples": 100.0
        }


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
                self.__tela.mostra_mensagem("Opção inválida.")

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")


    def buscar_quarto(self, numero: int) -> Quarto | None:
        for quarto in self.__quartos:
            if quarto.numero == numero:
                return quarto
        return None


    def cadastrar_quarto(self):
        try:
            dados = self.__tela.pega_dados_quarto()
            ValidacaoException.se_none(dados, "Dados inválidos.")

            numero = dados["numero"]

            if self.buscar_quarto(numero):
                raise ValidacaoException(f"O quarto nº {numero} já está cadastrado.")

            tipo = dados["tipo"]
            ClasseQuarto = self.__mapa_tipos.get(tipo)

            if not ClasseQuarto:
                raise ValidacaoException("Tipo de quarto inválido.")

            valor_diaria = self.__valores_diaria[tipo]
            disponibilidade = True

            if tipo == "suite":
                hidro = dados.get("hidro", False)
                quarto = ClasseQuarto(numero, disponibilidade, hidro)
            else:
                quarto = ClasseQuarto(numero, disponibilidade)

            quarto.valor_diaria = valor_diaria
            self.__quartos.append(quarto)

            self.__tela.mostra_mensagem(
                f"Quarto {quarto.numero} cadastrado com sucesso."
            )

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"Erro de validação: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado: {e}")


    def listar_quartos(self):
        if not self.__quartos:
            self.__tela.mostra_mensagem("Nenhum quarto cadastrado.")
            return

        lista = []

        for q in self.__quartos:
            tipo = type(q).__name__
            status = "Disponível" if q.disponibilidade else "Ocupado"

            hidro = ""
            if isinstance(q, Suite):
                hidro = f" | Hidro: {'Sim' if q.hidro else 'Não'}"

            lista.append(
                f"{tipo} nº {q.numero} | Diária: R${q.valor_diaria:.2f} | {status}{hidro}"
            )

        self.__tela.mostra_lista(lista)


    def alterar_quarto(self):
        try:
            numero = self.__tela.seleciona_quarto()
            quarto = self.buscar_quarto(numero)

            if not quarto:
                raise ValidacaoException("Quarto não encontrado.")

            tipo_existente = type(quarto).__name__.lower()

            novos_dados = self.__tela.pega_dados_quarto("alt", tipo_existente)

            ValidacaoException.se_none(novos_dados, "Dados inválidos.")

            disp_str = novos_dados["disponibilidade"].lower()
            if disp_str not in ["sim", "nao", "não"]:
                raise ValidacaoException("Disponibilidade deve ser 'sim' ou 'nao'.")
            quarto.disponibilidade = (disp_str == "sim")

            if isinstance(quarto, Suite):
                hidro_str = novos_dados["hidro"].lower()
                if hidro_str not in ["sim", "nao", "não"]:
                    raise ValidacaoException("Hidro deve ser 'sim' ou 'nao'.")
                quarto.hidro = (hidro_str == "sim")

            self.__tela.mostra_mensagem("Quarto alterado com sucesso.")

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"Erro de validação: {e}")


    def excluir_quarto(self):
        try:
            numero = self.__tela.seleciona_quarto()
            quarto = self.buscar_quarto(numero)

            if not quarto:
                raise ValidacaoException("Quarto não encontrado.")

            self.__quartos.remove(quarto)
            self.__tela.mostra_mensagem("Quarto excluído com sucesso.")

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")
