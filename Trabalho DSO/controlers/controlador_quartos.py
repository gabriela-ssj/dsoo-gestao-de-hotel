# controlers\controlador_quartos.py
from entidades.quarto import Quarto
from entidades.quartos import Suite, Duplo, Simples  # Importa os tipos específicos
from telas.tela_quarto import TelaQuarto


class ControladorQuarto:
    def __init__(self):
        self.__quartos: list[Quarto] = []
        self.__tela = TelaQuarto()
        self.__tipo_quartos_map = {
            "suite": {"class": Suite, "prefix": "S"},
            "duplo": {"class": Duplo, "prefix": "D"},
            "simples": {"class": Simples, "prefix": "Q"},
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
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")

    def cadastrar_quarto(self):
        dados = self.__tela.pega_dados_quarto()
        if not dados:  # Verifica se a tela retornou dados (ex: usuário cancelou)
            return

        tipo_quarto_info = self.__tipo_quartos_map.get(dados["tipo"])
        if not tipo_quarto_info:  # Validação redundante, mas segura caso a tela não valide
            self.__tela.mostra_mensagem("⚠️ Tipo de quarto inválido.")
            return

        numero_base = dados["numero"]

        if self.buscar_quarto(numero_base):
            self.__tela.mostra_mensagem(f"⚠️ Quarto {numero_base} já está cadastrado.")
            return

        QuartoClass = tipo_quarto_info["class"]
        try:
            if dados["tipo"] == "suite":
                quarto = QuartoClass(numero_base, dados["valor_diaria"], dados["disponibilidade"], dados["hidro"])
            else:
                quarto = QuartoClass(numero_base, dados["valor_diaria"], dados["disponibilidade"])

            self.__quartos.append(quarto)
            self.__tela.mostra_mensagem(f"✅ Quarto {quarto.numero} cadastrado com sucesso.")
        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro ao cadastrar quarto: {e}")
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
            hidro_info = ""
            if isinstance(q, Suite):
                hidro_info = f" | Hidro: {'Sim' if q.hidro else 'Não'}"

            lista.append(f"{tipo} nº {q.numero} | Diária: R${q.valor_diaria:.2f} | {status}{hidro_info}")
        self.__tela.mostra_lista(lista)

    def alterar_quarto(self):
        numero = self.__tela.seleciona_quarto()
        quarto = self.buscar_quarto(numero)
        if not quarto:
            self.__tela.mostra_mensagem(f"⚠️ Quarto {numero} não encontrado.")
            return

        novos_dados = self.__tela.pega_dados_quarto("alt")
        if not novos_dados:
            return
        #if novos_dados["tipo"].lower() != type(quarto).__name__.lower():
        #    self.__tela.mostra_mensagem("⚠️ Não é possível alterar o tipo de um quarto existente.")
        #    return

        try:
            quarto.valor_diaria = novos_dados["valor_diaria"]
            quarto.disponibilidade = novos_dados["disponibilidade"]

            if isinstance(quarto, Suite):
                if "hidro" in novos_dados:
                    quarto.hidro = novos_dados["hidro"]
                else:
                    hidro_str = self.__tela.le_string("Possui hidromassagem (sim/nao): ")
                    quarto.hidro = True if hidro_str.lower() == "sim" else False

            self.__tela.mostra_mensagem(f"✅ Quarto {quarto.numero} alterado com sucesso.")

        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro ao alterar quarto: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado: {e}")

    def excluir_quarto(self):
        numero = self.__tela.seleciona_quarto()
        quarto = self.buscar_quarto(numero)
        if quarto:
            self.__quartos.remove(quarto)
            self.__tela.mostra_mensagem(f"✅ Quarto {numero} excluído.")
        else:
            self.__tela.mostra_mensagem(f"⚠️ Quarto {numero} não encontrado.")

    def buscar_quarto(self, numero: int) -> Quarto:
        for q in self.__quartos:
            if q.numero == numero:
                return q
        return None