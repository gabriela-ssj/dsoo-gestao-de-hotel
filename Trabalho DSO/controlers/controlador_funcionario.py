from entidades.funcionario import Funcionario
from telas.tela_funcionario import TelaFuncionario 
from controlers.controlador_cargo import ControladorCargo 
from typing import List, Optional, Dict, Any

class ControladorFuncionario:
    def __init__(self, controlador_cargo: ControladorCargo):
        self.__tela = TelaFuncionario()
        self.__funcionarios: List[Funcionario] = []
        self.__controlador_cargo = controlador_cargo 

    def abre_tela(self):
        opcoes = {
            1: self.cadastrar_funcionario,
            2: self.listar_funcionarios,
            3: self.alterar_funcionario,
            4: self.excluir_funcionario,
            0: self.retornar
        }
        while True:
            opcao = self.__tela.tela_opcoes() 
            if opcao in opcoes:
                opcoes[opcao]()
                if opcao == 0:
                    break

    def retornar(self):
        """Método para retornar ao menu anterior."""
        pass 

    def cadastrar_funcionario(self):
        dados = self.__tela.pega_dados_funcionario(modo="cadastro") 
        if dados is None: 
            return

        cpf_novo = dados["cpf"]
        if self.buscar_funcionario(cpf_novo):
            self.__tela.mostra_mensagem(f"Funcionário com CPF {cpf_novo} já cadastrado.")
            return

        nome_cargo_digitado = dados["tipo_cargo"]
        cargo_selecionado = self.__controlador_cargo.buscar_cargo(nome_cargo_digitado)

        if not cargo_selecionado:
            self.__tela.mostra_mensagem(f"Cargo '{nome_cargo_digitado}' não encontrado. Por favor, cadastre o cargo primeiro.")
            return

        try:
            novo_funcionario = Funcionario(
                cpf=dados["cpf"],
                nome=dados["nome"],
                idade=dados["idade"],
                telefone=dados["telefone"],
                email=dados["email"],
                cargo=cargo_selecionado, 
                salario=dados["salario"]
            )
            self.__funcionarios.append(novo_funcionario)
            self.__tela.mostra_mensagem(f"Funcionário '{novo_funcionario.nome}' cadastrado com sucesso!")
        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro ao cadastrar funcionário: {e}")
        except TypeError as e: 
            self.__tela.mostra_mensagem(f"Erro de tipo ao cadastrar funcionário: {e}. Verifique o construtor.")

    def listar_funcionarios(self):
        if not self.__funcionarios:
            self.__tela.mostra_mensagem("Nenhum funcionário cadastrado.")
            return

        dados_para_tela = []
        for func in self.__funcionarios:
            dados_para_tela.append({
                "cpf": func.cpf,
                "nome": func.nome,
                "cargo_nome": func.cargo.tipo_cargo.capitalize(), 
                "salario": func.salario,
                "idade": func.idade,        
                "telefone": func.telefone,  
                "email": func.email         
            })
        self.__tela.mostra_funcionarios(dados_para_tela)

    def alterar_funcionario(self):
        cpf_para_alterar = self.__tela.seleciona_funcionario()
        if not cpf_para_alterar: 
            return

        funcionario_encontrado = self.buscar_funcionario(cpf_para_alterar)
        if not funcionario_encontrado:
            self.__tela.mostra_mensagem("Funcionário não encontrado.")
            return

        dados_atuais_func = {
            "cpf": funcionario_encontrado.cpf,
            "nome": funcionario_encontrado.nome,
            "cargo_nome": funcionario_encontrado.cargo.tipo_cargo, 
            "salario": funcionario_encontrado.salario,
            "idade": funcionario_encontrado.idade,         
            "telefone": funcionario_encontrado.telefone,   
            "email": funcionario_encontrado.email          
        }

        novos_dados = self.__tela.pega_dados_funcionario(modo="alteracao", dados_atuais=dados_atuais_func)
        if novos_dados is None:
            self.__tela.mostra_mensagem("Alteração de funcionário cancelada.")
            return

        if novos_dados["cpf"] != funcionario_encontrado.cpf:
            if self.buscar_funcionario(novos_dados["cpf"]):
                self.__tela.mostra_mensagem(f"Novo CPF '{novos_dados['cpf']}' já pertence a outro funcionário.")
                return

        novo_cargo_selecionado = self.__controlador_cargo.buscar_cargo(novos_dados["tipo_cargo"])
        if not novo_cargo_selecionado:
            self.__tela.mostra_mensagem(f"Cargo '{novos_dados['tipo_cargo']}' não encontrado. Alteração cancelada.")
            return

        try:
            funcionario_encontrado.cpf = novos_dados["cpf"]
            funcionario_encontrado.nome = novos_dados["nome"]
            funcionario_encontrado.idade = novos_dados["idade"]         
            funcionario_encontrado.telefone = novos_dados["telefone"]   
            funcionario_encontrado.email = novos_dados["email"]         
            funcionario_encontrado.cargo = novo_cargo_selecionado 
            funcionario_encontrado.salario = novos_dados["salario"]
            self.__tela.mostra_mensagem(f"Funcionário '{funcionario_encontrado.nome}' alterado com sucesso!")
        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro ao alterar funcionário: {e}")
        except TypeError as e:
            self.__tela.mostra_mensagem(f"Erro de tipo ao alterar funcionário: {e}. Verifique as propriedades.")

    def excluir_funcionario(self):
        """Permite ao usuário excluir um funcionário."""
        cpf_para_excluir = self.__tela.seleciona_funcionario()
        if not cpf_para_excluir: 
            return

        funcionario_encontrado = self.buscar_funcionario(cpf_para_excluir)
        if funcionario_encontrado:
            confirmacao = self.__tela.confirma_exclusao(funcionario_encontrado.nome, funcionario_encontrado.cpf)
            
            if confirmacao:
                self.__funcionarios.remove(funcionario_encontrado)
                self.__tela.mostra_mensagem(f"Funcionário '{funcionario_encontrado.nome}' excluído com sucesso.")
            else:
                self.__tela.mostra_mensagem("Exclusão de funcionário cancelada.")
        else:
            self.__tela.mostra_mensagem("Funcionário não encontrado.")

    def buscar_funcionario(self, cpf: str) -> Optional[Funcionario]:
        for funcionario in self.__funcionarios:
            if funcionario.cpf == cpf:
                return funcionario
        return None
