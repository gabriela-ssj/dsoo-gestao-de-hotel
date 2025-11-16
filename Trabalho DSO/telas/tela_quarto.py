from telas.tela_abstrata import TelaAbstrata

class TelaQuarto(TelaAbstrata):

    def tela_opcoes(self) -> int:
        print("\n------ MENU QUARTOS ------")
        print("1 - Cadastrar Quarto")
        print("2 - Listar Quartos")
        print("3 - Alterar Quarto")
        print("4 - Excluir Quarto")
        print("0 - Retornar")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1, 2, 3, 4])


    def pega_dados_quarto(self, modo: str = None, tipo_existente: str = None) -> dict:
        print("\n--- DADOS DO QUARTO ---")
        dados = {}

        if modo != "alt":
            tipo = self.le_string("Tipo do quarto (suite, duplo, simples): ").lower()

            while tipo not in ["suite", "duplo", "simples"]:
                self.mostra_mensagem("Tipo inválido! Escolha entre 'suite', 'duplo' ou 'simples'.")
                tipo = self.le_string("Tipo do quarto (suite, duplo, simples): ").lower()

            dados["tipo"] = tipo

            if tipo == "suite":
                hidro_str = self.le_string("Possui hidromassagem? (sim/nao): ").lower()

                while hidro_str not in ["sim", "nao", "não"]:
                    self.mostra_mensagem("⚠️ Entrada inválida! Digite apenas 'sim' ou 'nao'.")
                    hidro_str = self.le_string("Possui hidromassagem? (sim/nao): ").lower()

                dados["hidro"] = (hidro_str == "sim")

        dados["numero"] = self.le_num_inteiro("Número do quarto (ex: 101): ")

        if modo == "alt":
            disponibilidade_str = self.le_string("Disponível? (sim/nao): ").lower()

            while disponibilidade_str not in ["sim", "nao", "não"]:
                self.mostra_mensagem("⚠️ Entrada inválida! Digite apenas 'sim' ou 'nao'.")
                disponibilidade_str = self.le_string("Disponível? (sim/nao): ").lower()

            dados["disponibilidade"] = disponibilidade_str

            if tipo_existente == "suite":
                hidro_str = self.le_string("Possui hidromassagem? (sim/nao): ").lower()

                while hidro_str not in ["sim", "nao", "não"]:
                    self.mostra_mensagem("⚠️ Entrada inválida! Digite apenas 'sim' ou 'nao'.")
                    hidro_str = self.le_string("Possui hidromassagem? (sim/nao): ").lower()

                dados["hidro"] = hidro_str

        return dados


    def seleciona_quarto(self) -> int:
        return self.le_num_inteiro("Digite o número do quarto: ")

    def mostra_lista(self, lista: list):
        print("\n--- LISTA DE QUARTOS ---")
        if not lista:
            print("Nenhum quarto cadastrado.")
        else:
            for item in lista:
                print(item)
        print()

    def mostra_mensagem(self, msg: str):
        print(msg)
