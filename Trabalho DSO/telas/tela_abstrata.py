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
        valor = input(mensagem)
        return valor.strip().lower()

    def mostra_mensagem(self, mensagem: str):
        print(mensagem)

    def mostra_lista(self, lista: list):
        print("\n--- LISTA ---")
        for item in lista:
            print(item)

    @abstractmethod
    def tela_opcoes(self):
        pass
