# controlers/controlador_cargo.py

from entidades.cargo import Cargo
from telas.tela_cargo import TelaCargo
from typing import List, Optional

from controlers.ValidacaoException import ValidacaoException 


class ControladorCargo:
    def __init__(self):
        self.__tela = TelaCargo()
        self.__cargos: List[Cargo] = []
        self.populaCargos()

    def abre_tela(self):
        opcoes = {
            '1': self.listar_cargos_disponiveis,
            '2': self.criar_cargo_via_tela,
            '3': self.alterar_cargo_via_tela,
            '4': self.excluir_cargo_via_tela,
            '0': self.retornar
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao is None: # Se a tela não retornar nada, não processa.
                continue 
            
            funcao_escolhida = opcoes.get(opcao)
            if funcao_escolhida:
                if opcao == '0':
                    break
                funcao_escolhida()
            else:
                self.__tela.mostra_mensagem("Opção inválida.")
    
    def get_quantidade_cargos(self) -> int: 
        return len(self.__cargos)

    def buscar_cargo(self, tipo_cargo: str) -> Optional[Cargo]:
        """
        Busca um cargo na lista de cargos gerenciada pelo controlador.
        Retorna o objeto Cargo se encontrado, None caso contrário.
        """
        for cargo in self.__cargos:
            if cargo.tipo_cargo.lower() == tipo_cargo.lower():
                return cargo
        return None

    def retornar(self):
        """Método para retornar ao menu anterior (simplesmente sai do loop)."""
        pass 

    def listar_cargos_disponiveis(self):
        """Lista todos os cargos cadastrados exibindo-os na tela."""
        if not self.__cargos:
            self.__tela.mostra_mensagem("Nenhum cargo cadastrado.")
            return

        self.__tela.mostra_mensagem("--- LISTA DE CARGOS ---")
        lista_cargos_str = []
        for cargo in self.__cargos:
            lista_cargos_str.append(f"Tipo: {cargo.tipo_cargo.capitalize()} | Salário: R${cargo.salario_base:.2f}")
        self.__tela.mostra_lista(lista_cargos_str)


    def criar_cargo_via_tela(self):
        """
        Coleta dados da tela para criar um novo cargo.
        Utiliza adicionar_cargo_programaticamente para a lógica de negócio.
        """
        dados = self.__tela.pega_dados_cargo(modo="cadastro")
        if dados is None:
            return

        nome_cargo = dados["nome"]
        # O salário pego da tela é para ser usado se a classe Cargo puder ter salários personalizados.
        # Com sua classe Cargo atual, este 'salario_da_tela' será ignorado para o Cargo em si.
        # Se você quer que o salário da tela seja considerado, a classe Cargo precisaria de um __init__ diferente
        # ou de um setter para salario_base que pudesse ser chamado após a criação do Cargo.
        salario_da_tela = dados["salario"] 

        try:
            # Chama o método que adiciona o cargo.
            # O 'salario_da_tela' é passado, mas o Cargo.__init__ vai ignorá-lo e usar seu padrão.
            # Se você quer que 'salario_da_tela' seja o salário real, você precisará modificar a classe Cargo.
            self.adicionar_cargo_programaticamente(nome_cargo, salario_da_tela) 
            self.__tela.mostra_mensagem(f"Cargo '{nome_cargo.capitalize()}' criado com sucesso!")
        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f"Erro ao criar cargo: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao criar cargo: {e}")

    def adicionar_cargo_programaticamente(self, tipo_cargo: str, salario: float) -> Cargo:
        """
        Adiciona um novo cargo à lista de forma programática.
        Lança ValidacaoException se o cargo já existe ou os dados são inválidos.
        
        IMPORTANTE: Com a sua classe Cargo atual, o 'salario' passado a este método
        SERÁ IGNORADO pela instância de Cargo, que definirá seu próprio salario_base
        com base no tipo_cargo. Se você quer que 'salario' seja usado,
        a classe Cargo precisaria de um __init__ ou setter diferente.
        """
        if not isinstance(tipo_cargo, str) or not tipo_cargo.strip():
            raise ValidacaoException("Tipo de cargo deve ser uma string não vazia.")
        # Se você quer validar o salário MESMO que ele seja ignorado pela entidade Cargo, mantenha a validação abaixo
        if not isinstance(salario, (int, float)) or salario <= 0:
            raise ValidacaoException("Salário deve ser um número positivo.")

        if self.buscar_cargo(tipo_cargo):
            raise ValidacaoException(f"Cargo '{tipo_cargo.capitalize()}' já existe.")
        
        try:
            # CORREÇÃO PRINCIPAL AQUI: NÃO PASSE 'salario_base' para o construtor do Cargo.
            # O Cargo define seu próprio salário com base no tipo_cargo.
            novo_cargo = Cargo(tipo_cargo=tipo_cargo)
            # Se você tivesse um setter para salario_base na classe Cargo (como sugeri no Cenário 1),
            # e quisesse usar o 'salario' passado aqui, você faria:
            # novo_cargo.salario_base = salario 
            
            self.__cargos.append(novo_cargo)
            return novo_cargo
        except ValueError as e: # Captura ValueError que pode vir de Cargo.__init__
            raise ValidacaoException(f"Erro de validação na entidade Cargo: {e}") from e
        except Exception as e:
            raise ValidacaoException(f"Erro inesperado ao criar cargo internamente: {e}") from e
    
    def get_default_salario_for_cargo(self, tipo_cargo: str) -> float:
        """
        Retorna o salário base padrão para um determinado tipo de cargo.
        Se não encontrar, retorna um valor padrão (ex: 2000.0).
        """
        # AQUI estava usando _salarios_por_cargo_map, mas a classe Cargo usa _salarios_por_cargo
        # Você deve usar o dicionário da própria classe Cargo, não um atributo map que não existe lá.
        # E o acesso deve ser via Cargo._salarios_por_cargo, não self.__cargos[0]._salarios_por_cargo
        
        # CORREÇÃO: Acessar o dicionário estático da classe Cargo
        salario = Cargo._salarios_por_cargo.get(tipo_cargo.lower(), 2000.0)
        
        if salario <= 0:
            return 2000.0
        return salario

    def alterar_cargo_via_tela(self):
        """
        Coleta o nome do cargo a ser alterado e os novos dados via tela,
        depois aplica as alterações.
        """
        nome_cargo_para_alterar = self.__tela.seleciona_cargo()
        if not nome_cargo_para_alterar:
            self.__tela.mostra_mensagem("Alteração de cargo cancelada.")
            return

        cargo_encontrado = self.buscar_cargo(nome_cargo_para_alterar)

        if cargo_encontrado:
            # Se a classe Cargo não tiver um setter para salario_base, você não poderá alterá-lo diretamente
            # via cargo_encontrado.salario_base = novo_salario
            # O salário é sempre definido pelo tipo_cargo.
            # Então, ao alterar o nome do cargo, o salário também mudaria automaticamente.
            
            novos_dados = self.__tela.pega_dados_cargo(
                modo="alteracao",
                nome_atual=cargo_encontrado.tipo_cargo,
                salario_atual=cargo_encontrado.salario_base
            )
            if novos_dados is None:
                self.__tela.mostra_mensagem("Alteração de cargo cancelada.")
                return

            novo_nome = novos_dados["nome"]
            novo_salario = novos_dados["salario"] # Este novo_salario será 'ignorado' se Cargo não tiver setter

            try:
                # Se o nome do cargo for alterado para um tipo existente, o salario_base será atualizado
                # automaticamente via o setter de tipo_cargo na classe Cargo.
                if novo_nome.lower() != cargo_encontrado.tipo_cargo.lower():
                    if self.buscar_cargo(novo_nome):
                        raise ValidacaoException(f"Já existe um cargo com o nome '{novo_nome.capitalize()}'.")
                    
                    cargo_encontrado.tipo_cargo = novo_nome # Isso atualiza o tipo_cargo e salario_base
                
                # Se você realmente quer poder alterar o salário de um cargo individualmente,
                # e a classe Cargo tivesse um setter para salario_base (como sugeri no Cenário 1), faria:
                # cargo_encontrado.salario_base = novo_salario 
                # Mas, com sua classe Cargo atual, esta linha seria um AttributeError se você tentasse atribuir.
                # O salário é INTRÍNseco ao tipo_cargo.

                self.__tela.mostra_mensagem(f"Cargo alterado para '{novo_nome.capitalize()}' (Salário: R${cargo_encontrado.salario_base:.2f}).")
            except ValueError as e: # Captura ValueError que pode vir de Cargo.tipo_cargo.setter
                self.__tela.mostra_mensagem(f"Erro de validação ao alterar cargo: {e}")
            except ValidacaoException as e:
                self.__tela.mostra_mensagem(f"Erro de validação ao alterar cargo: {e}")
            except Exception as e:
                self.__tela.mostra_mensagem(f"Erro inesperado ao alterar cargo: {e}")
        else:
            self.__tela.mostra_mensagem(f"Cargo '{nome_cargo_para_alterar.capitalize()}' não encontrado.")

    def excluir_cargo_via_tela(self):
        """
        Coleta o nome do cargo a ser excluído via tela,
        solicita confirmação e então o remove.
        """
        nome_cargo_para_excluir = self.__tela.seleciona_cargo()
        if not nome_cargo_para_excluir:
            self.__tela.mostra_mensagem("Exclusão de cargo cancelada.")
            return

        cargo_encontrado = self.buscar_cargo(nome_cargo_para_excluir)

        if cargo_encontrado:
            confirmacao = self.__tela.confirma_acao(f"Tem certeza que deseja excluir o cargo '{nome_cargo_para_excluir.capitalize()}'?")
            if confirmacao:
                self.__cargos.remove(cargo_encontrado)
                self.__tela.mostra_mensagem(f"Cargo '{nome_cargo_para_excluir.capitalize()}' excluído.")
            else:
                self.__tela.mostra_mensagem("Operação de exclusão cancelada.")
        else:
            self.__tela.mostra_mensagem(f"Cargo '{nome_cargo_para_excluir.capitalize()}' não encontrado.")

    def _adicionar_cargo_diretamente(self, nome: str, salario: float) -> bool:
        """
        Método auxiliar interno para adicionar cargos sem interação com a tela,
        usado principalmente para popular a lista inicial.
        
        IMPORTANTE: O 'salario' é passado para adicionar_cargo_programaticamente,
        mas é ignorado pela instância de Cargo conforme sua implementação atual.
        """
        try:
            self.adicionar_cargo_programaticamente(nome, salario)
            return True
        except ValidacaoException as e:
            print(f"Erro interno ao popular cargo '{nome}': {e}")
            return False
        except Exception as e:
            # Captura exceções mais gerais aqui também, para depuração.
            print(f"Erro inesperado ao popular cargo '{nome}': {e}")
            return False

    def populaCargos(self):
        """Preenche a lista de cargos com alguns cargos iniciais."""
        cargos_iniciais = [
            ("gerente", 5000.0),
            ("recepcionista", 2500.0),
            ("camareira", 2200.0),
            ("cozinheira", 2300.0),
            ("limpeza", 2000.0),
            ("serviços gerais", 2100.0),
        ]
        for nome, salario in cargos_iniciais:
            self._adicionar_cargo_diretamente(nome, salario)
