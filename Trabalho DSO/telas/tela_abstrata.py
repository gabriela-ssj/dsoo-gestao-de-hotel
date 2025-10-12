from abc import ABC, abstractmethod

class TelaAbstrata(ABC):
    def le_num_inteiro(self, mensagem=" ", ints_validos=None):
        while True:
            valor_lido = input(mensagem)
            try:
                valor_int = int(valor_lido)
                if ints_validos and valor_int not in ints_validos:
                    raise ValueError
                return valor_int
            except ValueError:
                print("Valor incorreto!")
                if ints_validos:
                    print("Valores válidos:", ints_validos)

    def le_string(self, mensagem=" "):
        return input(mensagem).strip().lower()

    def le_float(self, mensagem=""):
        valor = input(mensagem)
        try:
            return float(valor)
        except ValueError:
            print("Valor inválido! Por favor, digite um número.")
        except Exception:
            print("Ocorreu um erro inesperado. Tente novamente.")

    def valida_cpf(self, mensagem="Digite o CPF (11 dígitos): "):
        while True:
            cpf = input(mensagem).strip()
            if cpf.isdigit() and len(cpf) == 11:
                return cpf
            print("⚠️ CPF inválido! Deve conter exatamente 11 números.")

    def mostra_mensagem(self, mensagem: str):
        print(mensagem)

    def mostra_lista(self, lista: list):
        print("\n--- LISTA ---")
        if not lista:
            print("Nenhum item para exibir.")
            return
        for item in lista:
            print(item)
        print()

    @abstractmethod
    def tela_opcoes(self):
        pass