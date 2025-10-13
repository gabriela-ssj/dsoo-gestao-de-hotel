# Arquivo: controlers/controlador_hospede.py

from typing import List, Optional

from entidades.hospede import Hospede
from telas.tela_hospede import TelaHospede
from controlers.controlador_pet import ControladorPet

# Se a classe Pet for usada diretamente aqui para tipagem ou outras operações, mantenha a importação.
# Se for usada apenas dentro de ControladorPet, pode ser movida para lá.
from entidades.pet import Pet


class ControladorHospede:
    def __init__(self):
        self.__hospedes: List[Hospede] = []
        self.__tela = TelaHospede()
        # Ao inicializar ControladorPet, ele pode precisar de uma referência ao ControladorHospede
        # para, por exemplo, associar pets a hóspedes existentes.
        self.__controlador_pet = ControladorPet(self) 

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")    

    def abre_tela(self):
        opcoes = {
            1: self.cadastrar_hospede_via_tela,
            2: self.listar_hospedes_via_tela,
            3: self.excluir_hospede_via_tela,
            4: self.alterar_hospede_via_tela,
            5: self.gerenciar_pets_via_tela,
            0: self.retornar
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao in opcoes:
                opcoes[opcao]()
                if opcao == 0:
                    break
            else:
                self.__tela.mostra_mensagem("⚠️ Opção inválida.")

    # Métodos adaptados para usar a tela

    def cadastrar_hospede_via_tela(self):
        # 1. Obtenha os dados do hóspede da tela
        dados = self.__tela.pega_dados_hospede()

        # Verificação: se a tela retornou None ou dicionário vazio (indicando cancelamento do usuário)
        if not dados:
            self.__tela.mostra_mensagem("Operação de cadastro de hóspede cancelada.")
            return

        # 2. Extraia o CPF para validação
        cpf_para_cadastro = dados["cpf"]
        
        # 3. Verifique se já existe um hóspede com esse CPF
        # Passamos o CPF diretamente para busca_hospede para evitar que ele peça novamente na tela
        hospede_existente = self.busca_hospede(cpf=cpf_para_cadastro)
        
        if hospede_existente:
            self.__tela.mostra_mensagem(f"⚠️ Erro: Já existe um hóspede cadastrado com o CPF '{cpf_para_cadastro}'.")
            return # Impede o cadastro se o CPF já existe
        
        # 4. Se o CPF é único, prossiga com a criação e cadastro do novo hóspede
        # Os dados já foram obtidos da tela, então use-os diretamente
        nome = dados["nome"]
        telefone = dados["telefone"]
        # Garante que idade é int, como esperado pelo construtor de Hospede
        idade = int(dados["idade"]) 
        email = dados["email"]
        
        hospede = Hospede(
            nome=nome,
            cpf=cpf_para_cadastro, # Usamos o CPF já validado
            telefone=telefone,
            idade=idade,
            email=email
        )
        self.cadastrar_hospede(hospede) # Chama o método interno para adicionar à lista
        self.__tela.mostra_mensagem(f"✅ Hóspede '{hospede.nome}' cadastrado com sucesso!")

    def alterar_hospede_via_tela(self):
        # Primeiro, busca o hóspede a ser alterado
        # A versão atualizada de busca_hospede pedirá o CPF se não for fornecido
        hospede = self.busca_hospede() 
        
        if hospede:
            # Pega os novos dados para alteração
            novos_dados = self.__tela.pega_dados_hospede(hospede_existente=hospede) 
            # Verifica se o usuário cancelou a entrada de novos dados
            if not novos_dados:
                self.__tela.mostra_mensagem("Operação de alteração cancelada.")
                return

            # Validação do CPF para alteração:
            # Se o CPF foi alterado e já existe no sistema (e não é o CPF do próprio hóspede que está sendo alterado)
            if novos_dados["cpf"] != hospede.cpf:
                hospede_com_novo_cpf = self.busca_hospede(cpf=novos_dados["cpf"])
                if hospede_com_novo_cpf:
                    self.__tela.mostra_mensagem(f"⚠️ Erro: O novo CPF '{novos_dados['cpf']}' já pertence a outro hóspede.")
                    return

            # Atualiza os atributos do objeto Hospede
            hospede.cpf = novos_dados["cpf"]
            hospede.nome = novos_dados["nome"]
            hospede.idade = int(novos_dados["idade"]) # Garante int
            hospede.telefone = novos_dados["telefone"]
            hospede.email = novos_dados["email"]

            self.__tela.mostra_mensagem("✅ Hóspede alterado com sucesso.")
        else:
            self.__tela.mostra_mensagem("⚠️ Hóspede não encontrado para alteração.")

    def cadastrar_hospede(self, hospede: Hospede):
        # Este método adiciona um objeto Hospede (já validado) à lista interna
        self.__hospedes.append(hospede)

    def listar_hospedes_via_tela(self):
        if not self.__hospedes:
            self.__tela.mostra_mensagem("Nenhum hóspede cadastrado.")
        else:
            lista = [f"{h.nome} | CPF: {h.cpf} | Idade: {h.idade}" for h in self.__hospedes]
            self.__tela.mostra_lista(lista)

    def excluir_hospede_via_tela(self):
        # Primeiro, busca o hóspede a ser excluído
        hospede_para_excluir = self.busca_hospede()
        
        if hospede_para_excluir:
            # Confirmação antes de excluir, boa prática
            confirmar = self.__tela.le_string(f"Deseja realmente excluir o hóspede {hospede_para_excluir.nome} (CPF: {hospede_para_excluir.cpf})? (sim/nao): ")
            if confirmar.lower() == "sim":
                self.excluir_hospede(hospede_para_excluir)
                self.__tela.mostra_mensagem(f"✅ Hóspede {hospede_para_excluir.nome} excluído com sucesso.")
            else:
                self.__tela.mostra_mensagem("Operação de exclusão cancelada.")
        else:
            self.__tela.mostra_mensagem("⚠️ Hóspede não encontrado para exclusão.")

    def busca_hospede(self, cpf: str = None) -> Optional[Hospede]:
        """
        Busca um hóspede pelo CPF.
        Se nenhum CPF for fornecido, solicita um à tela e continua pedindo até encontrar ou o usuário cancelar.
        Retorna o objeto Hospede se encontrado, caso contrário, retorna None.
        """
        hospede_encontrado = None
        cpf_para_buscar = cpf # Usa o CPF passado inicialmente, se houver

        # Primeiro, verifica se há algum hóspede cadastrado no sistema
        if not self.__hospedes:
            # Não exibe mensagem aqui se CPF foi passado, pois pode ser uma validação interna
            if cpf is None: # Apenas mostra mensagem se for uma busca interativa
                self.__tela.mostra_mensagem("Nenhum hóspede cadastrado no sistema.")
            return None # Retorna None se não há hóspedes para buscar

        # Loop para continuar pedindo o CPF até encontrar um hóspede ou o usuário cancelar (se busca interativa)
        while hospede_encontrado is None:
            # Se não foi fornecido um CPF inicial ou se a busca anterior falhou, ou se foi uma busca interativa
            if cpf_para_buscar is None:
                cpf_digitado_pelo_usuario = self.__tela.seleciona_hospede() # Pede o CPF
                if not cpf_digitado_pelo_usuario: # Se o usuário cancelar/não digitar
                    self.__tela.mostra_mensagem("Busca de hóspede cancelada.")
                    return None
                cpf_para_buscar = cpf_digitado_pelo_usuario

            # Percorre a lista de hóspedes para encontrar uma correspondência
            for hospede_obj in self.__hospedes:
                if hospede_obj.cpf == cpf_para_buscar:
                    hospede_encontrado = hospede_obj
                    break # Hóspede encontrado, sai do loop 'for'

            # Se o hóspede ainda não foi encontrado após o loop 'for'
            if hospede_encontrado is None:
                self.__tela.mostra_mensagem(f"⚠️ Hóspede com CPF '{cpf_para_buscar}' não encontrado. Por favor, tente novamente.")
                cpf_para_buscar = None # Zera o CPF para pedir novamente na próxima iteração do 'while'
                # Se a busca foi iniciada com um CPF específico (não interativa), deve sair aqui
                if cpf is not None: 
                    return None
            # Se hospede_encontrado não é None, o loop 'while' será encerrado.

        return hospede_encontrado


    def excluir_hospede(self, hospede: Hospede):
        # Este método remove um objeto Hospede (já validado) da lista interna
        if hospede:
            self.__hospedes.remove(hospede)
            self.__tela.mostra_mensagem(f"✅ Hóspede {hospede.nome} removido do sistema.")
        else:
            self.__tela.mostra_mensagem("⚠️ Erro: Objeto hóspede inválido para exclusão.")

    def gerenciar_pets_via_tela(self):
        # Delega o gerenciamento de pets para o controlador de pets
        self.__controlador_pet.abre_tela()
