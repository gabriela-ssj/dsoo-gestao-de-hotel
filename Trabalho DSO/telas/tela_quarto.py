from telas.tela_abstrata import TelaAbstrata

class TelaQuarto(TelaAbstrata):
    def tela_opcoes(self):
        print("\n------ MENU QUARTOS ------")
        print("1 - Cadastrar Quarto")
        print("2 - Listar Quartos")
        print("3 - Alterar Quarto")
        print("4 - Excluir Quarto")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])

    def pega_dados_quarto(self,tipo : str = None):
        print("\n--- DADOS DO QUARTO ---")
        if not(tipo == "alt"):
            tipo = self.le_string("Tipo do quarto (suite, duplo, simples): ")
            while tipo not in ["suite", "duplo", "simples"]:
                self.mostra_mensagem("Tipo de quarto inválido! Escolha entre 'suite', 'duplo' ou 'simples'.")
                tipo = self.le_string("Tipo do quarto (suite, duplo, simples): ")

        numero = self.le_num_inteiro("Número base do quarto (apenas números, ex: 101): ")
        valor_diaria = self.le_float("Valor da diária: ")
        disponibilidade_str = self.le_string("Disponibilidade (sim/nao): ")
        disponibilidade = True if disponibilidade_str == "sim" else False

        dados = {
            "tipo": tipo,
            "numero": numero,
            "valor_diaria": valor_diaria,
            "disponibilidade": disponibilidade
        }

        if tipo == "suite":
            hidro_str = self.le_string("Possui hidromassagem (sim/nao): ")
            dados["hidro"] = True if hidro_str == "sim" else False
        else:
            dados["hidro"] = False

        return dados

    def seleciona_quarto(self):
        return self.le_num_inteiro("Digite o número do quarto (ex: S101, D203, Q305): ")

    def mostra_lista(self, lista: list):
        print("\n--- LISTA DE QUARTOS ---")
        if not lista:
            print("Nenhum quarto cadastrado.")
            return
        for item in lista:
            print(item)
        print()

    def mostra_mensagem(self, msg: str):
        print(msg)