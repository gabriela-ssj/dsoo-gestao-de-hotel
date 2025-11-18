from entidades.funcionario import Funcionario
from entidades.cargo import Cargo
from telas.tela_funcionario import TelaFuncionario
from controlers.controlador_cargo import ControladorCargo
from controlers.ValidacaoException import ValidacaoException
from typing import List, Optional, Dict, Any


class ControladorFuncionario:
    def __init__(self, controlador_cargo: ControladorCargo):
        if not isinstance(controlador_cargo, ControladorCargo):
            raise TypeError("ControladorFuncionario deve ser inicializado com um objeto ControladorCargo.")

        self.__funcionarios: List[Funcionario] = []
        self.__controlador_cargo = controlador_cargo
        self.__tela = TelaFuncionario() 

    @property
    def funcionarios(self) -> List[Funcionario]:
        return list(self.__funcionarios)

    def abre_tela(self):
        opcoes = {
            '1': self.cadastrar_funcionario,
            '2': self.listar_funcionarios,
            '3': self.alterar_funcionario,
            '4': self.excluir_funcionario,
            '0': self.retornar
        }

        while True:
            opcao = self.__tela.tela_opcoes() 

            if not opcao and opcao != 0:
                self.__tela.mostra_mensagem("Opção inválida. Por favor, escolha uma das opções.")
                continue

            funcao_escolhida = opcoes.get(str(opcao))
            if funcao_escolhida:
                if opcao == 0:
                    break
                funcao_escolhida()
            else:
                self.__tela.mostra_mensagem("Opção inválida. Por favor, escolha uma das opções.")

    def retornar(self):
        pass

    def _buscar_funcionario_por_cpf(self, cpf: str) -> Funcionario:
        for funcionario in self.__funcionarios:
            if funcionario.cpf == cpf:
                return funcionario
        raise ValidacaoException(f"Funcionário com CPF {cpf} não encontrado.")

    def cadastrar_funcionario(self):
        try:
            dados = self.__tela.pega_dados_funcionario(modo="cadastro")
            ValidacaoException.se_none(dados, "Cadastro de funcionário cancelado pelo usuário.")
            ValidacaoException.validar_cpf_unico(self.__funcionarios, dados["cpf"])
            ValidacaoException.validar_campo_vazio(dados["nome"], "nome")
            ValidacaoException.validar_idade_valida(int(dados["idade"]))
            ValidacaoException.validar_email(dados["email"])
            ValidacaoException.validar_salario_valido(float(dados["salario"]))

            tipo_cargo_str = dados["tipo_cargo"]
            cargo = self.__controlador_cargo.buscar_cargo(tipo_cargo_str)

            if not cargo:
                self.__tela.mostra_mensagem(
                    f"Cargo '{tipo_cargo_str.capitalize()}' não encontrado. Criando automaticamente com salário padrão."
                )

                salario_base_para_cargo_novo = self.__controlador_cargo.get_default_salario_for_cargo(tipo_cargo_str)

                cargo = self.__controlador_cargo.adicionar_cargo_programaticamente(
                    tipo_cargo_str, salario_base_para_cargo_novo
                )
            
            salario_funcionario = float(dados["salario"]) 
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
            self.__tela.mostra_mensagem(f'Erro de validação: {e}')
        except ValueError as e:
            self.__tela.mostra_mensagem(f'Erro de formato nos dados: {e}. Verifique se idade e salário são números válidos.')
        except Exception as e:
            self.__tela.mostra_mensagem(f'Erro inesperado ao cadastrar funcionário: {e}')

    def listar_funcionarios(self):
        if not self.__funcionarios:
            self.__tela.mostra_mensagem("Nenhum funcionário cadastrado no momento.")
            return

        dados_para_exibir = [f.to_dict() for f in self.__funcionarios]
        self.__tela.mostra_funcionarios(dados_para_exibir) 

    def alterar_funcionario(self):
        try:
            cpf_para_alterar = self.__tela.seleciona_funcionario()
            ValidacaoException.se_none(cpf_para_alterar, "Alteração de funcionário cancelada.")

            funcionario_existente = self._buscar_funcionario_por_cpf(cpf_para_alterar)
            
            novos_dados = self.__tela.pega_dados_funcionario(
                modo="alteracao",
                dados_atuais=funcionario_existente.to_dict()
            )
            ValidacaoException.se_none(novos_dados, "Alteração de funcionário cancelada pelo usuário.")
            ValidacaoException.validar_campo_vazio(novos_dados["nome"], "nome")
            ValidacaoException.validar_idade_valida(int(novos_dados["idade"]))
            ValidacaoException.validar_email(novos_dados["email"])
            ValidacaoException.validar_salario_valido(float(novos_dados["salario"]))

            novo_tipo_cargo_str = novos_dados.get('tipo_cargo')
            novo_cargo_obj: Optional[Cargo] = None

            if novo_tipo_cargo_str and novo_tipo_cargo_str.lower() != funcionario_existente.cargo.tipo_cargo.lower():
                novo_cargo_obj = self.__controlador_cargo.buscar_cargo(novo_tipo_cargo_str)
                if not novo_cargo_obj:
                    self.__tela.mostra_mensagem(
                        f"Novo Cargo '{novo_tipo_cargo_str.capitalize()}' não encontrado. Criando automaticamente com salário padrão."
                    )
                    salario_base_para_cargo_novo = self.__controlador_cargo.get_default_salario_for_cargo(novo_tipo_cargo_str)

                    novo_cargo_obj = self.__controlador_cargo.adicionar_cargo_programaticamente(
                        novo_tipo_cargo_str, salario_base_para_cargo_novo
                    )
    
            funcionario_existente.nome = novos_dados["nome"]
            funcionario_existente.idade = int(novos_dados["idade"])
            funcionario_existente.telefone = novos_dados["telefone"]
            funcionario_existente.email = novos_dados["email"]
            funcionario_existente.salario = float(novos_dados["salario"])
            if novo_cargo_obj:
                funcionario_existente.cargo = novo_cargo_obj 

            self.__tela.mostra_mensagem(f"Funcionário {funcionario_existente.nome} alterado com sucesso!")

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f'Erro de validação: {e}')
        except ValueError as e:
            self.__tela.mostra_mensagem(f'Erro de formato nos dados: {e}. Verifique se idade e salário são números válidos.')
        except Exception as e:
            self.__tela.mostra_mensagem(f'Erro inesperado ao alterar funcionário: {e}')

    def excluir_funcionario(self):
        try:
            cpf_para_excluir = self.__tela.seleciona_funcionario()
            ValidacaoException.se_none(cpf_para_excluir, "Exclusão de funcionário cancelada.")

            funcionario_a_excluir = self._buscar_funcionario_por_cpf(cpf_para_excluir)

            if self.__tela.confirma_acao(f"Tem certeza que deseja excluir o funcionário {funcionario_a_excluir.nome} (CPF: {funcionario_a_excluir.cpf})?"):
                self.__funcionarios.remove(funcionario_a_excluir)
                self.__tela.mostra_mensagem(f"Funcionário {funcionario_a_excluir.nome} excluído com sucesso!")
            else:
                self.__tela.mostra_mensagem("Exclusão cancelada pelo usuário.")

        except ValidacaoException as e:
            self.__tela.mostra_mensagem(f'Erro de validação: {e}')
        except Exception as e:
            self.__tela.mostra_mensagem(f'Erro inesperado ao excluir funcionário: {e}')

    def buscar_funcionario(self, cpf: str) -> Optional[Funcionario]:
        for f in self.__funcionarios:
            if f.cpf == cpf:
                return f
        return None