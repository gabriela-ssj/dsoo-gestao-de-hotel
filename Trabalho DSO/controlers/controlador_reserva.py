from entidades.reserva import Reserva
from entidades.hospede import Hospede
from entidades.quarto import Quarto
from entidades.funcionario import Funcionario 
from entidades.servico_de_quarto import ServicoDeQuarto
from entidades.pet import Pet
from telas.tela_reserva import TelaReserva
from typing import List, Dict, Any, Optional
from datetime import datetime, date, timedelta

from controlers.controlador_hospede import ControladorHospede
from controlers.controlador_quartos import ControladorQuarto
from controlers.controlador_funcionario import ControladorFuncionario
from controlers.ValidacaoException import ValidacaoException
from controlers.ReservaException import ReservaException

class ControladorReserva:
    def __init__(self, controlador_hospede: ControladorHospede, controlador_quarto: ControladorQuarto,
                 controlador_funcionario: ControladorFuncionario):
        self.__reservas: List[Reserva] = []
        self.__tela = TelaReserva()
        self.__controlador_hospede = controlador_hospede
        self.__controlador_quarto = controlador_quarto
        self.__controlador_funcionario = controlador_funcionario

    def abre_tela(self):
        lista_opcoes = {
            1: self.fazer_reserva,
            2: self.listar_reservas,
            3: self.cancelar_reserva,
            4: self.alterar_reserva,
            5: self.adicionar_servico_quarto_reserva,
            6: self.adicionar_pet_reserva,
            7: self.mostrar_valor_total_reserva,
            8: self.gerar_relatorio_hospede,
            9: self.gerar_relatorio_tipo_servico,
            0: self.retornar
        }

        while True:
            try:
                opcao = self.__tela.tela_opcoes()
                funcao_escolhida = lista_opcoes.get(opcao)
                if funcao_escolhida:
                    funcao_escolhida()
                    if opcao == 0:
                        break
                else:
                    self.__tela.mostra_mensagem("Opção inválida. Por favor, escolha uma opção válida.")
            except ReservaException as e:
                self.__tela.mostra_mensagem(f"Erro de reserva: {e}")
            except ValidacaoException as e:
                self.__tela.mostra_mensagem(f"Erro de validação: {e}")
            except Exception as e:
                self.__tela.mostra_mensagem(f"Erro inesperado: {e}")

    def retornar(self):
        pass

    def fazer_reserva(self):
        try:
            dados_reserva = self.__tela.pega_dados_reserva()
            if not dados_reserva:
                raise ValidacaoException("Criação de reserva cancelada pelo usuário.")

            cpfs_hospedes = dados_reserva["hospedes_cpfs"]
            numeros_quartos = dados_reserva["quartos_ids"]
            checkin_data = dados_reserva["checkin_data"]
            checkout_data = dados_reserva["checkout_data"]

            hospedes_encontrados: List[Hospede] = []
            for cpf in cpfs_hospedes:
                hospede = self.__controlador_hospede.busca_hospede(cpf)
                if not hospede:
                    raise ReservaException(f"Hóspede com CPF {cpf} não encontrado. Reserva não pode ser criada.")
                hospedes_encontrados.append(hospede)

            if not hospedes_encontrados:
                raise ReservaException("Nenhum hóspede válido selecionado.")

            quartos_selecionados: List[Quarto] = []
            for num_quarto in numeros_quartos:
                quarto = self.__controlador_quarto.buscar_quarto(num_quarto)
                if not quarto:
                    raise ReservaException(f"Quarto {num_quarto} não existe.")

                if not quarto.disponibilidade:
                    raise ReservaException(f"Quarto {num_quarto} está indisponível.")

                quartos_selecionados.append(quarto)

            for quarto in quartos_selecionados:

                if not self.__controlador_quarto.verificar_disponibilidade_periodo(quarto, checkin_data, checkout_data):
                    raise ReservaException(f"Quarto {quarto.numero} não está disponível no período de {checkin_data.strftime('%d/%m/%Y')} a {checkout_data.strftime('%d/%m/%Y')}.")

            nova_reserva = Reserva(
                hospedes=hospedes_encontrados,
                quartos=quartos_selecionados,
                data_checkin=checkin_data,
                data_checkout=checkout_data
            )

            nova_reserva.reservar_quartos()

            self.__reservas.append(nova_reserva)
            self.__tela.mostra_mensagem(f"✅ Reserva ID {nova_reserva.id} criada com sucesso!")

        except (ValidacaoException, ReservaException) as e:
            self.__tela.mostra_mensagem(f"Erro ao fazer reserva: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao criar reserva: {e}")

    def selecionar_reserva(self) -> Optional[Reserva]:
        """
        Consolida a busca de reserva por ID ou por nome do hóspede principal,
        com tratamento de exceções robusto.
        """
        try:
            identificador = self.__tela.seleciona_reserva()
            if not identificador:
                raise ValidacaoException("Seleção de reserva cancelada pelo usuário.")

            try:
                reserva_id = int(identificador)
                for reserva in self.__reservas:
                    if reserva.id == reserva_id:
                        return reserva
                raise ReservaException("Reserva não encontrada com o ID fornecido.")
            except ValueError:
                reservas_encontradas = [
                    r for r in self.__reservas
                    if r.hospedes and identificador.lower() in r.hospedes[0].nome.lower()
                ]

                if len(reservas_encontradas) == 1:
                    return reservas_encontradas[0]
                elif len(reservas_encontradas) > 1:
                    raise ReservaException("Múltiplas reservas encontradas para o nome do hóspede. Por favor, use o ID da reserva.")
                else:
                    raise ReservaException("Nenhuma reserva encontrada para o nome do hóspede fornecido.")

        except (ValidacaoException, ReservaException) as e:
            self.__tela.mostra_mensagem(f"Erro ao selecionar reserva: {e}")
            return None
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao buscar reserva: {e}")
            return None

    def listar_reservas(self):
        if not self.__reservas:
            self.__tela.mostra_mensagem("Nenhuma reserva cadastrada.")
            return
        
        reservas_para_exibir = [reserva.get_all_data() for reserva in self.__reservas]
        self.__tela.mostra_reservas(reservas_para_exibir)

    def cancelar_reserva(self):
        try:
            reserva = self.selecionar_reserva()
            if not reserva:
                return

            hospedes_nomes = ", ".join([h.nome for h in reserva.hospedes])
            if self.__tela.confirma_cancelamento(reserva.id, hospedes_nomes):
                reserva.status = "cancelada"
                reserva.liberar_quartos()
                self.__tela.mostra_mensagem(f"✅ Reserva ID {reserva.id} cancelada com sucesso!")
            else:
                raise ValidacaoException("Cancelamento da reserva não confirmado pelo usuário.")

        except (ValidacaoException, ReservaException) as e:
            self.__tela.mostra_mensagem(f"Erro ao cancelar reserva: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao cancelar reserva: {e}")


    def alterar_reserva(self):
        try:
            reserva = self.selecionar_reserva()
            if not reserva:
                return
            
            hospedes_nomes = ", ".join([h.nome for h in reserva.hospedes])
            if not self.__tela.confirma_edicao(reserva.id, hospedes_nomes):
                raise ValidacaoException("Edição da reserva não confirmada pelo usuário.")

            dados_atuais = {
                "hospedes_cpfs": [h.cpf for h in reserva.hospedes],
                "quartos_ids": [q.numero for q in reserva.quartos],
                "checkin": reserva.data_checkin,
                "checkout": reserva.data_checkout
            }

            novos_dados_reserva = self.__tela.pega_dados_reserva(modo="alteracao", dados_atuais=dados_atuais)

            if not novos_dados_reserva:
                raise ValidacaoException("Alteração da reserva cancelada ou dados inválidos.")

            novos_cpfs_hospedes = novos_dados_reserva["hospedes_cpfs"]
            novos_numeros_quartos = novos_dados_reserva["quartos_ids"]
            nova_checkin_data = novos_dados_reserva["checkin_data"]
            nova_checkout_data = novos_dados_reserva["checkout_data"]

            novos_hospedes_encontrados: List[Hospede] = []
            for cpf in novos_cpfs_hospedes:
                hospede = self.__controlador_hospede.busca_hospede(cpf)
                if not hospede:
                    raise ReservaException(f"Hóspede com CPF {cpf} não encontrado. Alteração não pode ser concluída.")
                novos_hospedes_encontrados.append(hospede)

            novos_quartos_encontrados: List[Quarto] = []
            for num_quarto in novos_numeros_quartos:
                quarto = self.__controlador_quarto.buscar_quarto(num_quarto)
                if not quarto:
                    raise ReservaException(f"Quarto com número {num_quarto} não encontrado. Alteração não pode ser concluída.")
                
                if not quarto.disponibilidade and quarto not in reserva.quartos:
                    raise ReservaException(f"Quarto {num_quarto} não está disponível. Alteração não pode ser concluída.")
                
                if not self.__controlador_quarto.verificar_disponibilidade_periodo(quarto, nova_checkin_data, nova_checkout_data, reserva_sendo_editada=reserva):
                    raise ReservaException(f"Quarto {quarto.numero} não está disponível no período de {nova_checkin_data.strftime('%d/%m/%Y')} a {nova_checkout_data.strftime('%d/%m/%Y')}.")

                novos_quartos_encontrados.append(quarto)

            reserva.editar_reserva(
                nova_data_checkin=nova_checkin_data,
                nova_data_checkout=nova_checkout_data,
                novos_quartos=novos_quartos_encontrados,
                novos_hospedes=novos_hospedes_encontrados
            )

            self.__tela.mostra_mensagem(f"Reserva ID {reserva.id} alterada com sucesso! Novo valor: R\$ {reserva.valor_total:.2f}")

        except (ValidacaoException, ReservaException) as e:
            self.__tela.mostra_mensagem(f"Erro ao alterar reserva: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao alterar reserva: {e}")


    def adicionar_servico_quarto_reserva(self):
        try:
            reserva = self.selecionar_reserva()
            if not reserva:
                return

            dados_servico = self.__tela.pega_dados_servico_quarto()
            if not dados_servico:
                raise ValidacaoException("Adição de serviço de quarto cancelada ou dados inválidos.")

            cpf_funcionario = dados_servico["cpf_funcionario"]
            funcionario = self.__controlador_funcionario.buscar_funcionario(cpf_funcionario)
            if not funcionario:
                raise ReservaException(f"Funcionário com CPF {cpf_funcionario} não encontrado.")

            num_quarto = dados_servico["num_quarto"]
            quarto_encontrado: Optional[Quarto] = None
            for quarto_reserva in reserva.quartos:
                if quarto_reserva.numero == num_quarto:
                    quarto_encontrado = quarto_reserva
                    break
            
            if not quarto_encontrado:
                raise ReservaException(f"Quarto {num_quarto} não faz parte da Reserva ID {reserva.id}.")

            novo_servico = ServicoDeQuarto(
                tipo_servico=dados_servico["tipo_servico"],
                valor=dados_servico["valor"],
                quarto=quarto_encontrado,
                funcionario=funcionario
            )
            reserva.adicionar_servico_quarto(novo_servico)
            
            self.__tela.mostra_mensagem(f"Serviço '{novo_servico.tipo_servico}' adicionado à Reserva ID {reserva.id}. Novo valor total: R\$ {reserva.valor_total:.2f}")

        except (ValidacaoException, ReservaException) as e:
            self.__tela.mostra_mensagem(f"Erro ao adicionar serviço de quarto: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao adicionar serviço de quarto: {e}")

    def adicionar_pet_reserva(self):
        try:
            reserva = self.selecionar_reserva()
            if not reserva:
                return
            
            dados_pet = self.__tela.pega_dados_pet()
            if not dados_pet:
                raise ValidacaoException("Adição de pet cancelada ou dados inválidos.")
            
            novo_pet = Pet(nome_pet=dados_pet["nome_pet"], especie=dados_pet["especie"])
            reserva.adicionar_pet(novo_pet) 
            
            self.__tela.mostra_mensagem(f"Pet '{novo_pet.nome_pet}' adicionado à Reserva ID {reserva.id}. Novo valor total: R\$ {reserva.valor_total:.2f}")

        except (ValidacaoException, ReservaException) as e:
            self.__tela.mostra_mensagem(f"Erro ao adicionar pet: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao adicionar pet: {e}")

    def mostrar_valor_total_reserva(self):
        try:
            reserva = self.selecionar_reserva()
            if not reserva:
                return 

            self.__tela.mostra_valor_total(reserva.id, reserva.valor_total)

        except (ValidacaoException, ReservaException) as e:
            self.__tela.mostra_mensagem(f"Erro ao mostrar valor total da reserva: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao mostrar valor total da reserva: {e}")

    def gerar_relatorio_hospede(self):
        try:
            if not self.__reservas:
                raise ValidacaoException("Nenhuma reserva cadastrada para gerar relatório.")

            cpf_hospede = self.__tela.pega_cpf_hospede_relatorio()
            if not cpf_hospede:
                raise ValidacaoException("Geração de relatório por hóspede cancelada.")

            hospede_alvo = self.__controlador_hospede.busca_hospede(cpf_hospede)
            if not hospede_alvo:
                raise ReservaException(f"Hóspede com CPF {cpf_hospede} não encontrado.")

            reservas_do_hospede = []
            for reserva in self.__reservas:
                for hospede_na_reserva in reserva.hospedes:
                    if hospede_na_reserva.cpf == cpf_hospede:
                        reservas_do_hospede.append(reserva.get_all_data())
                        break

            self.__tela.mostra_relatorio_hospede(cpf_hospede, reservas_do_hospede)

        except (ValidacaoException, ReservaException) as e:
            self.__tela.mostra_mensagem(f"Erro ao gerar relatório por hóspede: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao gerar relatório por hóspede: {e}")

    def gerar_relatorio_tipo_servico(self):
        try:
            if not self.__reservas:
                raise ValidacaoException("Nenhuma reserva cadastrada para gerar relatório.")

            tipo_servico = self.__tela.pega_tipo_servico_relatorio()
            if not tipo_servico:
                raise ValidacaoException("Geração de relatório por tipo de serviço cancelada.")
            
            servicos_do_tipo = []
            for reserva in self.__reservas:
                for servico in reserva.servicos_quarto:
                    if servico.tipo_servico.lower() == tipo_servico.lower():
                        
                        servicos_do_tipo.append({
                            "reserva_id": reserva.id,
                            "tipo": servico.tipo_servico,
                            "valor": servico.valor,
                            "num_quarto": servico.quarto.numero if servico.quarto else "N/A",
                            "funcionario_nome": servico.funcionario.nome if servico.funcionario else "N/A",
                            "funcionario_cpf": servico.funcionario.cpf if servico.funcionario else "N/A"
                        })
            
            if not servicos_do_tipo:
                 self.__tela.mostra_mensagem(f"Nenhum serviço do tipo '{tipo_servico}' encontrado.")
                 return

            self.__tela.mostra_relatorio_servico(tipo_servico, servicos_do_tipo)

        except (ValidacaoException, ReservaException) as e:
            self.__tela.mostra_mensagem(f"Erro ao gerar relatório por tipo de serviço: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao gerar relatório por tipo de serviço: {e}")

    @property
    def reservas(self) -> List[Reserva]:
        return self.__reservas
