from entidades.servico_de_quarto import ServicoDeQuarto
from telas.tela_servicodequarto import TelaServicoDeQuarto
from typing import Optional, Dict, Any, List


class ControladorServicoDeQuarto:
    def __init__(self, controlador_quarto, controlador_funcionario):
        self.__servicos: list[ServicoDeQuarto] = []
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
            self.__tela.mostra_mensagem("Solicitação de serviço cancelada ou dados de entrada inválidos.")
            return
            
        try:
            numero_quarto = int(dados["numero_quarto"])
            quarto = self.__controlador_quarto.buscar_quarto(numero_quarto)

            cpf = dados["cpf_funcionario"]
            funcionario = self.__controlador_funcionario.buscar_funcionario(cpf)

            if not quarto:
                self.__tela.mostra_mensagem(f"Quarto {numero_quarto} não encontrado.")
                return

            if not funcionario:
                self.__tela.mostra_mensagem(f"Funcionário com CPF {cpf} não encontrado.")
                return

            servico = ServicoDeQuarto(quarto, funcionario, dados["tipo_servico"], dados["valor"])
            self.__servicos.append(servico)
            self.__tela.mostra_mensagem(f"Serviço '{servico.tipo_servico}' solicitado para o quarto {quarto.numero} e será atendido por {funcionario.nome}.")

        except ValueError:
            self.__tela.mostra_mensagem("Erro: O número do quarto e o CPF devem ser valores numéricos válidos.")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao solicitar serviço: {e}")


    def listar_servicos(self):
        if not self.__servicos:
            self.__tela.mostra_mensagem("Nenhum serviço registrado.")
            return
            
        lista_para_gui: List[Dict[str, Any]] = []

        for s in self.__servicos:
            lista_para_gui.append({
                "numero_quarto": s.quarto.numero,
                "nome_funcionario": s.funcionario.nome,
                "tipo_servico": s.tipo_servico,
                "valor": s.valor,
                "status": s.status
            })

        self.__tela.mostra_lista(lista_para_gui)

    def alterar_status_servico(self):
        numero_quarto_str = self.__tela.seleciona_servico()
        
        if numero_quarto_str is None:
            self.__tela.mostra_mensagem("Busca de serviço cancelada.")
            return

        servico = next((s for s in self.__servicos if str(s.quarto.numero) == numero_quarto_str), None)
        
        if not servico:
            self.__tela.mostra_mensagem(f"Serviço não encontrado para o quarto {numero_quarto_str}.")
            return

        novo_status = self.__tela.seleciona_status()
        
        if novo_status is None:
            self.__tela.mostra_mensagem("Alteração de status cancelada.")
            return
            
        try:
            servico.status = novo_status
            self.__tela.mostra_mensagem(f"Status do serviço no quarto {servico.quarto.numero} alterado para '{novo_status.capitalize()}'.")
        except ValueError as e:
            self.__tela.mostra_mensagem(str(e))
