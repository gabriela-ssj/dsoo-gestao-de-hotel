class TelaSistema:
    def tela_opcoes(self):
        print("\n--- MENU PRINCIPAL DO SISTEMA DE HOTÉIS ---")
        print("1 - Gerenciar Hotéis")
        print("0 - Sair")
        return int(input("Escolha a opção: "))

    def mostra_mensagem(self, msg):
        print(msg)
