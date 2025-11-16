class TelaCargo:
    def __init__(self):
        pass

    def tela_opcoes(self):
        """Exibe as opções do menu de cargos e retorna a escolha do usuário."""
        print("-------- MENU CARGOS ----------")
        print("1 - Listar Cargos Disponíveis")
        print("2 - Criar Cargo")
        print("3 - Alterar Cargo")
        print("4 - Excluir Cargo")
        print("0 - Retornar")
        try:
            opcao = int(input("Escolha a opção: "))
            return opcao
        except ValueError:
            self.mostra_mensagem("Entrada inválida. Digite um número inteiro.")
            return -1

    def pega_dados_cargo(self, modo="cadastro", nome_atual=None, salario_atual=None):
        """
        Coleta os dados de um cargo do usuário.
        No modo "alteracao", permite manter o valor atual se o campo for deixado vazio.
        """
        dados = {}
        
        if modo == "cadastro":
            nome_prompt = "Digite o nome do cargo: "
            salario_prompt = "Digite o salario: "
        else:
            nome_prompt = f"Digite o novo nome do cargo (Atual: {nome_atual.capitalize()}): "
            salario_prompt = f"Digite o novo salário (Atual: R\${salario_atual:.2f}): "

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
                    self.mostra_mensagem("Criação de cargo cancelada.")
                    return None
            
            try:
                salario = float(salario_str.replace(',', '.'))
                if salario < 0:
                    raise ValueError("Salário deve ser positivo.")
            except ValueError:
                self.mostra_mensagem("Valor inválido! Por favor, digite um número positivo válido.")
        
        dados["nome"] = nome
        dados["salario"] = salario
        return dados

    def seleciona_cargo(self):
        """Solicita ao usuário o nome de um cargo para seleção."""
        nome = input("Digite o nome do cargo: ").strip()
        return nome

    def mostra_mensagem(self, mensagem: str):
        """Exibe uma mensagem para o usuário."""
        print(mensagem)

    def mostra_lista(self, lista: list):
        """Exibe uma lista de itens para o usuário."""
        if not lista:
            print("--- Lista vazia ---")
            return
        for item in lista:
            print(item)
