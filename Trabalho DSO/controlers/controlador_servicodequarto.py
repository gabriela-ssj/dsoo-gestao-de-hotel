from entidades.servico_de_quarto import ServicoDeQuarto
from telas.tela_servicodequarto import TelaServicoDeQuarto
from daos.servicodequarto_dao import ServicoDeQuartoDAO
from typing import Optional, Dict, Any, List


class ControladorServicoDeQuarto:
    def __init__(self, controlador_quarto, controlador_funcionario):
        self.__dao = ServicoDeQuartoDAO()
        self.__tela = TelaServicoDeQuarto()
        self.__controlador_quarto = controlador_quarto
        self.__controlador_funcionario = controlador_funcionario

    def abre_tela(self):
        opcoes = {
            1: self.solicitar_servico,
            2: self.listar_servicos,
            3: self.alterar_status_servico,
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

    def solicitar_servico(self):
        dados: Optional[Dict[str, Any]] = self.__tela.pega_dados_servico()
        
        if dados is None:
            self.__tela.mostra_mensagem("Solicitação cancelada.")
            return
            
        try:
            numero_quarto = int(dados["numero_quarto"])
            quarto = self.__controlador_quarto.buscar_quarto(numero_quarto)

            cpf = dados["cpf_funcionario"]
            funcionario = self.__controlador_funcionario.buscar_funcionario(cpf)

            if not quarto:
                self.__tela.mostra_mensagem("Quarto não encontrado.")
                return

            if not funcionario:
                self.__tela.mostra_mensagem("Funcionário não encontrado.")
                return

            servico = ServicoDeQuarto(
                quarto,
                funcionario,
                dados["tipo_servico"],
                dados["valor"]
            )

            self.__dao.add(servico)

            self.__tela.mostra_mensagem(
                f"Serviço '{servico.tipo_servico}' registrado para o quarto {quarto.numero}."
            )

        except ValueError:
            self.__tela.mostra_mensagem("Erro: número do quarto / CPF inválidos.")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado: {e}")

    def listar_servicos(self):
        servicos = self.__dao.get_all()

        if not servicos:
            self.__tela.mostra_mensagem("Nenhum serviço registrado.")
            return

        lista_gui: List[Dict[str, Any]] = []

        for s in servicos:
            lista_gui.append({
                "numero_quarto": s.quarto.numero,
                "nome_funcionario": s.funcionario.nome,
                "tipo_servico": s.tipo_servico,
                "valor": s.valor,
                "status": s.status
            })

        self.__tela.mostra_lista(lista_gui)

    def alterar_status_servico(self):
        numero_quarto_str = self.__tela.seleciona_servico()

        if numero_quarto_str is None:
            self.__tela.mostra_mensagem("Operação cancelada.")
            return

        try:
            numero_quarto = int(numero_quarto_str)
        except ValueError:
            self.__tela.mostra_mensagem("Número inválido.")
            return

        servico = self.__dao.get(numero_quarto)

        if not servico:
            self.__tela.mostra_mensagem("Serviço não encontrado.")
            return

        novo_status = self.__tela.seleciona_status()

        if novo_status is None:
            self.__tela.mostra_mensagem("Alteração cancelada.")
            return

        try:
            servico.status = novo_status
            self.__dao.update(servico)
            self.__tela.mostra_mensagem(
                f"Status alterado para '{novo_status.capitalize()}'."
            )
        except ValueError as e:
            self.__tela.mostra_mensagem(str(e))
