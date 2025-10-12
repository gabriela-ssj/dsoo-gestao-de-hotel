from entidades.quartos import Suite, Duplo, Simples
from entidades.quarto import Quarto
from telas.tela_quarto import TelaQuarto

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
        "duplo": 180.0,
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
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")

    def buscar_quarto(self, numero: int) -> Quarto | None:
        for quarto in self.__quartos:
            if quarto.numero == numero:
                return quarto
            return None    

    def cadastrar_quarto(self):
        dados = self.__tela.pega_dados_quarto()
        if not dados:
            return
        
        if self.buscar_quarto(dados["numero"]):
            self.__tela.mostra_mensagem("⚠️ Quarto já cadastrado.")
            return
        
        tipo = dados["tipo"]
        ClasseQuarto = self.__mapa_tipos.get(tipo)
        if not ClasseQuarto:
            self.__tela.mostra_mensagem("⚠️ Tipo de quarto inválido.")
            return
        
        valor_diaria = self.__valores_diaria.get(tipo)
        self.__tela.mostra_mensagem(f"ℹ️ Valor da diária para tipo '{tipo}': R$ {valor_diaria:.2f}")
        
        try:
            if tipo == "suite":
                quarto = ClasseQuarto(dados["numero"], valor_diaria, dados["disponibilidade"], dados["hidro"])
            else:
                quarto = ClasseQuarto(dados["numero"], valor_diaria, dados["disponibilidade"])
            self.__quartos.append(quarto)
            self.__tela.mostra_mensagem(f"✅ Quarto {quarto.numero} cadastrado com sucesso.")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")

    def listar_quartos(self):
        if not self.__quartos:
            self.__tela.mostra_mensagem("Nenhum quarto cadastrado.")
            return

        lista = []
        for q in self.__quartos:
            tipo = type(q).__name__
            status = "Disponível" if q.disponibilidade else "Ocupado"
            hidro = f" | Hidro: {'Sim' if isinstance(q, Suite) and q.hidro else 'Não'}"
            lista.append(f"{tipo} nº {q.numero} | Diária: R${q.valor_diaria:.2f} | {status}{hidro if isinstance(q, Suite) else ''}")
        self.__tela.mostra_lista(lista)

    def alterar_quarto(self):
        numero = self.__tela.seleciona_quarto()
        quarto = self.buscar_quarto(numero)
        if not quarto:
            self.__tela.mostra_mensagem("⚠️ Quarto não encontrado.")
            return
        
        novos_dados = self.__tela.pega_dados_quarto("alt")
        try:
            quarto.disponibilidade = novos_dados["disponibilidade"]
            if isinstance(quarto, Suite):
                quarto.hidro = novos_dados.get("hidro", False)
            self.__tela.mostra_mensagem("✅ Quarto alterado com sucesso.")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro: {e}")

    def excluir_quarto(self):
        numero = self.__tela.seleciona_quarto()
        quarto = self.buscar_quarto(numero)
        if quarto:
            self.__quartos.remove(quarto)
            self.__tela.mostra_mensagem("✅ Quarto excluído.")
        else:
            self.__tela.mostra_mensagem("⚠️ Quarto não encontrado.")
