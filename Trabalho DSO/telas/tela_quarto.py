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

    def pega_dados_quarto(self, modo: str = None) -> dict:
        print("\n--- DADOS DO QUARTO ---")
        tipo = None
        valor_diaria = None

        if modo != "alt":
            tipo = self.le_string("Tipo do quarto (suite, duplo, simples): ").lower()
            while tipo not in ["suite", "duplo", "simples"]:
                self.mostra_mensagem("⚠️ Tipo inválido! Escolha entre 'suite', 'duplo' ou 'simples'.")
                tipo = self.le_string("Tipo do quarto (suite, duplo, simples): ").lower()

            # Informar valor fixo da diária
            valores_fixos = {
                "suite": 300.0,
                "duplo": 180.0,
                "simples": 100.0
            }
            valor_diaria = valores_fixos[tipo]
            self.mostra_mensagem(f"ℹ️ Valor da diária para '{tipo}': R$ {valor_diaria:.2f}")

        numero = self.le_num_inteiro("Número base do quarto (ex: 101): ")
        disponibilidade_str = self.le_string("Disponível? (sim/nao): ").lower()
        disponibilidade = disponibilidade_str == "sim"

        dados = {
            "tipo": tipo,
            "numero": numero,
            "valor_diaria": valor_diaria,
            "disponibilidade": disponibilidade
        }

        if tipo == "suite":
            hidro_str = self.le_string("Possui hidromassagem? (sim/nao): ").lower()
            dados["hidro"] = hidro_str == "sim"
        else:
            dados["hidro"] = False

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
