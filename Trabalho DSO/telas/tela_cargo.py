from typing import Dict, Any, Optional, List

class TelaCargo:
    def __init__(self):
        pass

    def tela_opcoes(self) -> str:
        """Exibe as opções do menu de cargos e retorna a escolha do usuário como string."""
        print("-------- MENU CARGOS ----------")
        print("1 - Listar Cargos Disponíveis")
        print("2 - Criar Cargo")
        print("3 - Alterar Cargo")
        print("4 - Excluir Cargo")
        print("0 - Retornar")
        
        opcao = input("Escolha a opção: ").strip()
        return opcao

    def pega_dados_cargo(self, modo: str = "cadastro", nome_atual: Optional[str] = None, salario_atual: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """
        Coleta os dados de um cargo do usuário.
        No modo "alteracao", permite manter o valor atual se o campo for deixado vazio.
        """
        dados = {}
        
        if modo == "cadastro":
            nome_prompt = "Digite o nome do cargo: "
            salario_prompt = "Digite o salario: "
        else:
            nome_display = nome_atual.capitalize() if nome_atual else ""
            salario_display = f"{salario_atual:.2f}" if salario_atual is not None else ""
            nome_prompt = f"Digite o novo nome do cargo (Atual: {nome_display}): "
            salario_prompt = f"Digite o novo salário (Atual: R\${salario_display}): "

        nome = input(nome_prompt).strip()
        if not nome:
            if modo == "alteracao":
                nome = nome_atual
            else:
                self.mostra_mensagem("Nome do cargo é obrigatório. Operação cancelada.")
                return None

        salario = None
        while salario is None:
            salario_str = input(salario_prompt).strip()
            if not salario_str:
                if modo == "alteracao":
                    salario = salario_atual
                    break
                else:
                    self.mostra_mensagem("Salário é obrigatório na criação. Operação cancelada.")
                    return None
            
            try:
                salario = float(salario_str.replace(',', '.'))
                if salario <= 0:
                    raise ValueError("Salário deve ser um número positivo.")
            except ValueError as e:
                self.mostra_mensagem(f"Valor inválido: {e}. Por favor, digite um número positivo válido.")
        
        dados["nome"] = nome
        dados["salario"] = salario
        return dados

    def seleciona_cargo(self) -> str:
        """Solicita ao usuário o nome de um cargo para seleção."""
        nome = input("Digite o nome do cargo: ").strip()
        return nome

    def mostra_mensagem(self, mensagem: str):
        """Exibe uma mensagem para o usuário."""
        print(mensagem)

    def mostra_lista(self, lista: List[str]):
        """Exibe uma lista de itens para o usuário."""
        if not lista:
            print("--- Lista vazia ---")
            return
        for item in lista:
            print(item)

    def confirma_acao(self, mensagem: str) -> bool:
        """Solicita confirmação do usuário via console."""
        while True:
            resposta = input(f"{mensagem} (sim/nao): ").strip().lower()
            if resposta == "sim":
                return True
            elif resposta == "nao":
                return False
            else:
                print("Resposta inválida. Por favor, digite 'sim' ou 'nao'.")
