from entidades.funcionario import Funcionario
from telas.tela_funcionario import TelaFuncionario 
from controlers.controlador_cargo import ControladorCargo 
from typing import List, Optional, Dict, Any
from controlers.controlador_cargo import ControladorCargo
from telas.tela_funcionario import TelaFuncionario
from controlers.ValidacaoException import ValidacaoException


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
        try:
            dados = self.__tela.pega_dados_funcionario()
            ValidacaoException.se_none(dados, "Dados não fornecidos.")

            ValidacaoException.validar_campo_vazio(dados["nome"], "nome")
            ValidacaoException.validar_cpf_unico(self.__funcionarios, dados["cpf"])
            ValidacaoException.validar_idade_valida(int(dados["idade"]))
            ValidacaoException.validar_email(dados["email"])

            tipo_cargo_str = dados["tipo_cargo"]
            cargo = self.__controlador_cargo.buscar_cargo(tipo_cargo_str)
            

            salario_funcionario: float = 0.0
            if 'salario' in dados and dados['salario']:
                salario_funcionario = float(dados['salario'])
            
            if not cargo:
                self.__tela.mostra_mensagem(
                    f"Cargo '{tipo_cargo_str}' não encontrado. Criando automaticamente..."
                )

                salario_base_para_cargo_novo = Cargo._salarios_por_cargo_map.get(tipo_cargo_str.lower(), 2000.0)
                if salario_base_para_cargo_novo <= 0:
                    raise ValidacaoException(f"Não foi possível determinar um salário base válido para o cargo '{tipo_cargo_str}'.")

                cargo = self.__controlador_cargo.criar_cargo(
                    tipo_cargo_str, salario_base_para_cargo_novo
                )

                if not ('salario' in dados and dados['salario']):
                    salario_funcionario = cargo.salario_base

            else:

                if not ('salario' in dados and dados['salario']):
                    salario_funcionario = cargo.salario_base
            
            ValidacaoException.validar_salario_valido(salario_funcionario)

            funcionario = Funcionario(
                nome=dados["nome"],
                cpf=dados["cpf"],
                idade=int(dados["idade"]),
                telefone=dados["telefone"],
                email=dados["email"],
                cargo=cargo,
                salario=salario_funcionario
            )

            self.__funcionarios.append(funcionario)
            self.__tela.mostra_mensagem(f"Funcionário {funcionario.nome} cadastrado com sucesso!")

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f'Erro: {e}')
        except ValueError as e:
            self.__tela.mostra_mensagem(f'Erro de formato nos dados: {e}')
        except Exception as e:
            self.__tela.mostra_mensagem(f'Erro inesperado ao cadastrar funcionário: {e}')
