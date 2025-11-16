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
            opcao = self.__tela.tela_opcoes()
            funcao_escolhida = lista_opcoes.get(opcao)
            if funcao_escolhida:
                funcao_escolhida()
                if opcao == 0:
                    break
            else:
                self.__tela.mostra_mensagem("Opção inválida. Por favor, escolha uma opção válida.")

    def retornar(self):
        pass

    def fazer_reserva(self):
        dados_reserva = self.__tela.pega_dados_reserva()

        if dados_reserva is None:
            self.__tela.mostra_mensagem("Criação de reserva cancelada ou dados inválidos.")
            return

        cpfs_hospedes = dados_reserva["hospedes_cpfs"]
        numeros_quartos = dados_reserva["quartos_ids"]
        checkin_data = dados_reserva["checkin_data"]
        checkout_data = dados_reserva["checkout_data"]

        hospedes_encontrados: List[Hospede] = []
        for cpf in cpfs_hospedes:
            hospede = self.__controlador_hospede.busca_hospede(cpf)
            if hospede:
                hospedes_encontrados.append(hospede)
            else:
                self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf} não encontrado. Reserva não pode ser criada.")
                return

        quartos_encontrados: List[Quarto] = []
        for num_quarto in numeros_quartos:
            quarto = self.__controlador_quarto.buscar_quarto(num_quarto)
            if quarto:
                if quarto.disponibilidade: 
                    quartos_encontrados.append(quarto)
                else:
                    self.__tela.mostra_mensagem(f"Quarto {num_quarto} não está disponível. Reserva não pode ser criada.")
                    return
            else:
                self.__tela.mostra_mensagem(f"Quarto com número {num_quarto} não encontrado. Reserva não pode ser criada.")
                return
        
        try:
            nova_reserva = Reserva(
                hospedes=hospedes_encontrados,
                quartos=quartos_encontrados,
                data_checkin=checkin_data,
                data_checkout=checkout_data
            )
            self.__reservas.append(nova_reserva)
            nova_reserva.reservar_quartos()
            self.__tela.mostra_mensagem(f"Reserva ID {nova_reserva.id} criada com sucesso! Valor inicial: R\$ {nova_reserva.valor_total:.2f}")

        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro nos dados da reserva: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao criar reserva: {e}")

    def busca_reserva_por_id(self, id_reserva: int) -> Optional[Reserva]:
        for reserva in self.__reservas:
            if reserva.id == id_reserva:
                return reserva
        return None

    def busca_reservas_por_hospede_principal(self, nome_hospede: str) -> List[Reserva]:
        reservas_encontradas = []
        for reserva in self.__reservas:
            for hospede in reserva.hospedes:
                if nome_hospede.lower() in hospede.nome.lower():
                    reservas_encontradas.append(reserva)
                    break
        return reservas_encontradas

    def selecionar_reserva(self) -> Optional[Reserva]:
        identificador = self.__tela.seleciona_reserva()
        if identificador is None:
            self.__tela.mostra_mensagem("Seleção de reserva cancelada.")
            return None

        try:
            reserva_id = int(identificador)
            reserva = self.busca_reserva_por_id(reserva_id)
            if not reserva:
                self.__tela.mostra_mensagem("Reserva não encontrada com o ID fornecido.")
                return None
            return reserva
        except ValueError:
            reservas_por_nome = self.busca_reservas_por_hospede_principal(identificador)
            if not reservas_por_nome:
                self.__tela.mostra_mensagem("Nenhuma reserva encontrada para o nome do hóspede fornecido.")
                return None
            elif len(reservas_por_nome) == 1:
                return reservas_por_nome[0]
            else:
                self.__tela.mostra_mensagem("Múltiplas reservas encontradas. Por favor, use o ID da reserva.")
                return None

    def listar_reservas(self):
        reservas_para_exibir = [reserva.get_all_data() for reserva in self.__reservas]
        self.__tela.mostra_reservas(reservas_para_exibir)

    def cancelar_reserva(self):
        reserva = self.selecionar_reserva()
        if not reserva:
            return

        hospedes_nomes = ", ".join([h.nome for h in reserva.hospedes])
        if self.__tela.confirma_cancelamento(reserva.id, hospedes_nomes):
            reserva.status = "cancelada"
            reserva.liberar_quartos()
            self.__tela.mostra_mensagem(f"Reserva ID {reserva.id} cancelada com sucesso!")
        else:
            self.__tela.mostra_mensagem("Cancelamento da reserva não confirmado.")

    def alterar_reserva(self):
        reserva = self.selecionar_reserva()
        if not reserva:
            return
        
        hospedes_nomes = ", ".join([h.nome for h in reserva.hospedes])
        if not self.__tela.confirma_edicao(reserva.id, hospedes_nomes):
            self.__tela.mostra_mensagem("Edição da reserva não confirmada.")
            return

        dados_atuais = {
            "hospedes_cpfs": [h.cpf for h in reserva.hospedes],
            "quartos_ids": [q.numero for q in reserva.quartos],
            "checkin": reserva.data_checkin,
            "checkout": reserva.data_checkout
        }

        novos_dados_reserva = self.__tela.pega_dados_reserva(modo="alteracao", dados_atuais=dados_atuais)

        if novos_dados_reserva is None:
            self.__tela.mostra_mensagem("Alteração da reserva cancelada ou dados inválidos.")
            return

        novos_cpfs_hospedes = novos_dados_reserva["hospedes_cpfs"]
        novos_numeros_quartos = novos_dados_reserva["quartos_ids"]
        nova_checkin_data = novos_dados_reserva["checkin_data"]
        nova_checkout_data = novos_dados_reserva["checkout_data"]

        novos_hospedes_encontrados: List[Hospede] = []
        for cpf in novos_cpfs_hospedes:
            hospede = self.__controlador_hospede.busca_hospede(cpf)
            if hospede:
                novos_hospedes_encontrados.append(hospede)
            else:
                self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf} não encontrado. Alteração não pode ser concluída.")
                return

        novos_quartos_encontrados: List[Quarto] = []
        for num_quarto in novos_numeros_quartos:
            quarto = self.__controlador_quarto.buscar_quarto(num_quarto)
            if quarto:
                if quarto.disponibilidade or quarto in reserva.quartos:
                    novos_quartos_encontrados.append(quarto)
                else:
                    self.__tela.mostra_mensagem(f"Quarto {num_quarto} não está disponível. Alteração não pode ser concluída.")
                    return
            else:
                self.__tela.mostra_mensagem(f"Quarto com número {num_quarto} não encontrado. Alteração não pode ser concluída.")
                return

        try:
            reserva.editar_reserva(
                nova_data_checkin=nova_checkin_data,
                nova_data_checkout=nova_checkout_data,
                novos_quartos=novos_quartos_encontrados,
                novos_hospedes=novos_hospedes_encontrados
            )

            self.__tela.mostra_mensagem(f"Reserva ID {reserva.id} alterada com sucesso! Novo valor: R\$ {reserva.valor_total:.2f}")

        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro ao alterar reserva: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao alterar reserva: {e}")


    def adicionar_servico_quarto_reserva(self):
        reserva = self.selecionar_reserva()
        if not reserva:
            return

        dados_servico = self.__tela.pega_dados_servico_quarto()
        if dados_servico is None:
            self.__tela.mostra_mensagem("Adição de serviço de quarto cancelada ou dados inválidos.")
            return

        cpf_funcionario = dados_servico["cpf_funcionario"]
        funcionario = self.__controlador_funcionario.buscar_funcionario(cpf_funcionario)
        if not funcionario:
            self.__tela.mostra_mensagem(f"Funcionário com CPF {cpf_funcionario} não encontrado.")
            return

        num_quarto = dados_servico["num_quarto"]
        quarto_encontrado: Optional[Quarto] = None
        for quarto_reserva in reserva.quartos:
            if quarto_reserva.numero == num_quarto:
                quarto_encontrado = quarto_reserva
                break
        
        if not quarto_encontrado:
            self.__tela.mostra_mensagem(f"Quarto {num_quarto} não faz parte da Reserva ID {reserva.id}.")
            return

        try:
            novo_servico = ServicoDeQuarto(
                tipo_servico=dados_servico["tipo_servico"],
                valor=dados_servico["valor"],
                quarto=quarto_encontrado,
                funcionario=funcionario
            )
            reserva.adicionar_servico_quarto(novo_servico)

            self.__tela.mostra_mensagem(f"Serviço '{novo_servico.tipo_servico}' adicionado à Reserva ID {reserva.id}. Novo valor total: R\$ {reserva.valor_total:.2f}")

        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro ao adicionar serviço de quarto: {e}")

    def adicionar_pet_reserva(self):
        reserva = self.selecionar_reserva()
        if not reserva:
            return
        
        dados_pet = self.__tela.pega_dados_pet()
        if dados_pet is None:
            self.__tela.mostra_mensagem("Adição de pet cancelada ou dados inválidos.")
            return
        
        try:
            novo_pet = Pet(nome_pet=dados_pet["nome_pet"], especie=dados_pet["especie"])
            reserva.adicionar_pet(novo_pet) 
            
            self.__tela.mostra_mensagem(f"Pet '{novo_pet.nome_pet}' adicionado à Reserva ID {reserva.id}. Novo valor total: R\$ {reserva.valor_total:.2f}")

        except KeyError as ke:
            self.__tela.mostra_mensagem(f"Erro nos dados do pet (chave ausente): {ke}. Verifique se a TelaReserva retorna as chaves 'nome_pet' e 'especie'.")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao adicionar pet: {e}")

    def mostrar_valor_total_reserva(self):
        reserva = self.selecionar_reserva()
        if not reserva:
            return

        self.__tela.mostra_valor_total(reserva.id, reserva.valor_total)

    def gerar_relatorio_hospede(self):
        cpf_hospede = self.__tela.pega_cpf_hospede_relatorio()
        if not cpf_hospede:
            return

        hospede_alvo = self.__controlador_hospede.busca_hospede(cpf_hospede)
        if not hospede_alvo:
            self.__tela.mostra_mensagem(f"Hóspede com CPF {cpf_hospede} não encontrado.")
            return

        reservas_do_hospede = []
        for reserva in self.__reservas:
            for hospede_na_reserva in reserva.hospedes:
                if hospede_na_reserva.cpf == cpf_hospede:
                    reservas_do_hospede.append(reserva.get_all_data())
                    break

        self.__tela.mostra_relatorio_hospede(cpf_hospede, reservas_do_hospede)

    def gerar_relatorio_tipo_servico(self):
        tipo_servico = self.__tela.pega_tipo_servico_relatorio()
        if not tipo_servico:
            return
        
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
        
        self.__tela.mostra_relatorio_servico(tipo_servico, servicos_do_tipo)
