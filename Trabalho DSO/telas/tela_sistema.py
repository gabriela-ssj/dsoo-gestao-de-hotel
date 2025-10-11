class TelaSistema(TelaAbstrata):
    def tela_opcoes(self):
        print("-------- MENU PRINCIPAL DO SISTEMA DE HOTÉIS ---------")
        print("Escolha sua opcao")
        print("1 - Gerenciar Hotéis")
        print("0 - Sair do sistema")
        return self.le_num_inteiro("Escolha a opção: ", [0, 1])
    
    def mostra_mensagem(self, msg):
        print(msg)
