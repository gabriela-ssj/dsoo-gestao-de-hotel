from entidades.reserva import Reserva
from entidades.servico_de_quarto import ServicoDeQuarto
from entidades.pet import Pet
from telas.tela_reserva import TelaReserva
from controlers.controlador_hospede import ControladorHospede
from controlers.controlador_quartos import ControladorQuarto
from controlers.controlador_funcionario import ControladorFuncionario
from datetime import datetime
from typing import List, Optional


class ControladorReserva:
    def __init__(self, controlador_hospede: ControladorHospede, controlador_quarto: ControladorQuarto,
                 controlador_funcionario: ControladorFuncionario):
        self.__reservas: list[Reserva] = []
        self.__tela = TelaReserva()
        self.__controlador_hospede = controlador_hospede
        self.__controlador_quarto = controlador_quarto
        self.__controlador_funcionario = controlador_funcionario

    def abre_tela(self):
        opcoes = {
            1: self.fazer_reserva,
            2: self.listar_reservas,
            3: self.cancelar_reserva,
            4: self.editar_reserva,
            5: self.adicionar_servico_a_reserva,
            6: self.adicionar_pet_a_reserva,
            7: self.calcular_valor_total_reserva,  # Modificado para calcular de uma reserva específica
            8: self.exibir_relatorio_por_hospede,
            9: self.exibir_relatorio_por_tipo_servico,
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

    def retornar(self):
        self.__tela.mostra_mensagem("Retornando ao menu anterior...")

    def fazer_reserva(self):
        dados_reserva = self.__tela.pega_dados_reserva()
        if not dados_reserva:
            self.__tela.mostra_mensagem("Criação de reserva cancelada.")
            return

        # 1. Buscar Hóspedes
        hospedes_encontrados = []
        for cpf in dados_reserva["cpfs_hospedes"]:
            hospede = self.__controlador_hospede.busca_hospede(cpf)
            if hospede:
                hospedes_encontrados.append(hospede)
            else:
                self.__tela.mostra_mensagem(f"⚠️ Hóspede com CPF {cpf} não encontrado. Reserva não pode ser criada.")
                return

        if not hospedes_encontrados:
            self.__tela.mostra_mensagem("⚠️ Nenhum hóspede válido selecionado para a reserva.")
            return

        # 2. Buscar Quartos e Validar Disponibilidade
        quartos_selecionados = []
        for numero_quarto in dados_reserva["numeros_quartos"]:
            quarto = self.__controlador_quarto.buscar_quarto(int(numero_quarto))
            if quarto:
                if quarto.disponibilidade:
                    quartos_selecionados.append(quarto)
                else:
                    self.__tela.mostra_mensagem(
                        f"⚠️ Quarto {numero_quarto} não está disponível. Reserva não pode ser criada.")
                    return
            else:
                self.__tela.mostra_mensagem(f"⚠️ Quarto {numero_quarto} não encontrado. Reserva não pode ser criada.")
                return

        if not quartos_selecionados:
            self.__tela.mostra_mensagem("⚠️ Nenhum quarto válido selecionado para a reserva.")
            return

        try:
            nova_reserva = Reserva(
                hospedes=hospedes_encontrados,
                quartos=quartos_selecionados,
                data_checkin=dados_reserva["data_checkin"],
                data_checkout=dados_reserva["data_checkout"]
            )
            # Tentar reservar os quartos
            if not nova_reserva.reservar_quartos():
                self.__reservas.append(nova_reserva)
                self.__tela.mostra_mensagem(f"✅ Reserva ID {nova_reserva.id} criada com sucesso!")
                self.__tela.mostra_mensagem(nova_reserva.get_all_data())
            else:
                self.__tela.mostra_mensagem(f"Reserva não pode ser criada.")

        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro ao criar reserva: {e}")
        except TypeError as e:
            self.__tela.mostra_mensagem(f"Erro nos dados da reserva: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao criar reserva: {e}")

    def listar_reservas(self):
        if not self.__reservas:
            self.__tela.mostra_mensagem("Nenhuma reserva cadastrada.")
            return

        lista_str = [str(reserva) for reserva in self.__reservas]
        self.__tela.mostra_lista_reservas(lista_str)

    def _selecionar_reserva(self,reserva_identificador = None) -> Optional[Reserva]:
        if not reserva_identificador:
            reserva_identificador = self.__tela.seleciona_reserva()
        if not reserva_identificador:
            self.__tela.mostra_mensagem("Seleção de reserva cancelada.")
            return None

        # Tentar buscar por ID (se for numérico)
        try:
            reserva_id = int(reserva_identificador)
            for reserva in self.__reservas:
                if reserva.id == reserva_id:
                    return reserva
        except ValueError:
            # Se não for numérico, buscar por parte do nome do hóspede principal
            encontradas = [
                reserva for reserva in self.__reservas
                if reserva.hospedes and reserva_identificador.lower() in reserva.hospedes[0].nome.lower()
            ]
            if len(encontradas) == 1:
                return encontradas[0]
            elif len(encontradas) > 1:
                self.__tela.mostra_mensagem(
                    "⚠️ Múltiplas reservas encontradas. Por favor, seja mais específico ou use o ID da reserva.")
                self.__tela.mostra_lista_reservas([str(r) for r in encontradas])
                return None

        self.__tela.mostra_mensagem(f"⚠️ Nenhuma reserva encontrada com o identificador '{reserva_identificador}'.")
        return None

    def cancelar_reserva(self):
        reserva_para_cancelar = self._selecionar_reserva()
        if reserva_para_cancelar:
            confirmar = self.__tela.le_string("Tem certeza que deseja cancelar esta reserva? (sim/nao): ")
            if confirmar.lower() == 'sim':
                try:
                    reserva_para_cancelar.liberar_quartos()
                    self.__reservas.remove(reserva_para_cancelar)
                    self.__tela.mostra_mensagem(f"✅ Reserva ID {reserva_para_cancelar.id} cancelada com sucesso.")
                except Exception as e:
                    self.__tela.mostra_mensagem(f"Erro ao cancelar reserva: {e}")
            else:
                self.__tela.mostra_mensagem("Cancelamento de reserva não confirmado.")

    def editar_reserva(self):
        reserva_para_editar = self._selecionar_reserva()
        if not reserva_para_editar:
            return

        self.__tela.mostra_mensagem(f"Editando Reserva ID {reserva_para_editar.id}:")
        self.__tela.mostra_detalhes_reserva({
            "ID": reserva_para_editar.id,
            "Hóspedes": ", ".join([h.nome for h in reserva_para_editar.hospedes]),
            "Quartos": ", ".join([str(q.numero) for q in reserva_para_editar.quartos]),
            "Check-in Atual": reserva_para_editar.data_checkin.strftime("%d/%m/%Y"),
            "Check-out Atual": reserva_para_editar.data_checkout.strftime("%d/%m/%Y"),
            "Status Atual": reserva_para_editar.status
        })

        dados_edicao = self.__tela.pega_dados_edicao()
        if not dados_edicao:
            self.__tela.mostra_mensagem("Edição de reserva cancelada.")
            return

        novos_quartos_obj = None
        if dados_edicao["limpar_quartos"]:
            novos_quartos_obj = []
            self.__tela.mostra_mensagem("Quartos da reserva serão removidos.")
        elif dados_edicao["novos_numeros_quartos"]:
            novos_quartos_obj = []
            for num_quarto in dados_edicao["novos_numeros_quartos"]:
                quarto = self.__controlador_quarto.buscar_quarto(int(num_quarto))
                if quarto:
                    if quarto.disponibilidade or quarto in reserva_para_editar.quartos:  # Pode ser o mesmo quarto
                        novos_quartos_obj.append(quarto)
                    else:
                        self.__tela.mostra_mensagem(
                            f"⚠️ Quarto {num_quarto} não disponível ou não encontrado. Edição cancelada.")
                        return
                else:
                    self.__tela.mostra_mensagem(f"⚠️ Quarto {num_quarto} não encontrado. Edição cancelada.")
                    return

        try:
            reserva_para_editar.editar_reserva(
                nova_data_checkin=dados_edicao["nova_data_checkin"],
                nova_data_checkout=dados_edicao["nova_data_checkout"],
                novos_quartos=novos_quartos_obj
            )
            self.__tela.mostra_mensagem(f"✅ Reserva ID {reserva_para_editar.id} alterada com sucesso!")
            self.__tela.mostra_mensagem(str(reserva_para_editar))

        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro ao editar reserva: {e}")
        except TypeError as e:
            self.__tela.mostra_mensagem(f"Erro nos dados da edição: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao editar reserva: {e}")

    def adicionar_servico_a_reserva(self):
        reserva_alvo = self._selecionar_reserva()
        if not reserva_alvo:
            return

        dados_servico = self.__tela.pega_dados_servico()
        if not dados_servico:
            self.__tela.mostra_mensagem("Adição de serviço cancelada.")
            return

        # 1. Buscar Quarto na Reserva
        quarto_para_servico = None
        for q in reserva_alvo.quartos:
            if q.numero == int(dados_servico["numero_quarto"]):
                quarto_para_servico = q
                break
        if not quarto_para_servico:
            self.__tela.mostra_mensagem(f"⚠️ Quarto {dados_servico['numero_quarto']} não faz parte desta reserva.")
            return

        # 2. Buscar Funcionário
        funcionario_responsavel = self.__controlador_funcionario.buscar_funcionario(dados_servico["cpf_funcionario"])
        if not funcionario_responsavel:
            self.__tela.mostra_mensagem(f"⚠️ Funcionário com CPF {dados_servico['cpf_funcionario']} não encontrado.")
            return

        try:
            novo_servico = ServicoDeQuarto(
                quarto=quarto_para_servico,
                funcionario=funcionario_responsavel,
                tipo_servico=dados_servico["tipo_servico"],
                valor=dados_servico["valor"]
            )
            reserva_alvo.adicionar_servico_quarto(novo_servico)
            self.__tela.mostra_mensagem(
                f"✅ Serviço '{novo_servico.tipo_servico}' adicionado à Reserva ID {reserva_alvo.id}.")
        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro ao adicionar serviço: {e}")
        except TypeError as e:
            self.__tela.mostra_mensagem(f"Erro nos dados do serviço: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao adicionar serviço: {e}")

    def adicionar_pet_a_reserva(self):
        reserva_alvo = self._selecionar_reserva()
        if not reserva_alvo:
            return

        hospedes = reserva_alvo.hospedes
        qtn_pet = 0
        for hospede in hospedes:
            qtn_pet += len(hospede.pets)

        if qtn_pet == 0:
            self.__tela.mostra_mensagem("Nenhum pet cadastrado nos hospedes da reserva")
            self.__controlador_hospede.gerenciar_pets_via_tela()

        qtn_pet = 0
        for hospede in hospedes:
            qtn_pet += len(hospede.pets)
        if qtn_pet == 0:
            return

        hospede = self.__controlador_hospede.busca_hospede()
        nome_pet = self.__tela.le_string("Qual o nome do pet")
        pet = hospede.busca_pet(nome_pet)
        try:
            reserva_alvo.adicionar_pet(pet)
            self.__tela.mostra_mensagem(f"✅ Pet '{pet.nome_pet}' adicionado à Reserva ID {reserva_alvo.id}.")

            # Tenta adicionar o pet aos quartos da reserva. O quarto fará sua própria validação.
            for quarto in reserva_alvo.quartos:
                if quarto.adicionar_pet(pet):
                    self.__tela.mostra_mensagem(f"  > Pet '{pet.nome_pet}' alocado no Quarto {quarto.numero}.")
                else:
                    self.__tela.mostra_mensagem(
                        f"  > ⚠️ Quarto {quarto.numero} não pode acomodar o pet '{pet.nome_pet}'.")

        except ValueError as e:
            self.__tela.mostra_mensagem(f"Erro ao adicionar pet: {e}")
        except TypeError as e:
            self.__tela.mostra_mensagem(f"Erro nos dados do pet: {e}")
        except Exception as e:
            self.__tela.mostra_mensagem(f"Erro inesperado ao adicionar pet: {e}")

    def calcular_valor_total_reserva(self):
        reserva_alvo = self._selecionar_reserva()
        if not reserva_alvo:
            return

        reserva_alvo.calcular_valor_total()
        self.__tela.mostra_mensagem(
            f"✅ O valor total para a Reserva ID {reserva_alvo.id} é: R$ {reserva_alvo.valor_total:.2f}")

    def exibir_relatorio_por_hospede(self):
        # Implementação mais complexa, pode precisar de agregação de dados
        # Fornece um resumo simples para cada hóspede
        if not self.__reservas:
            self.__tela.mostra_mensagem("Nenhuma reserva para gerar relatório.")
            return

        relatorio = []
        hospedes_com_reservas = {}  # {cpf: [reserva_id, reserva_id], ...}

        for reserva in self.__reservas:
            for hospede in reserva.hospedes:
                if hospede.cpf not in hospedes_com_reservas:
                    hospedes_com_reservas[hospede.cpf] = {"nome": hospede.nome, "reservas_ids": []}
                hospedes_com_reservas[hospede.cpf]["reservas_ids"].append(reserva.id)

        for cpf, info in hospedes_com_reservas.items():
            relatorio.append(
                f"Hóspede: {info['nome']} (CPF: {cpf}) | Reservas IDs: {', '.join(map(str, info['reservas_ids']))}")

        self.__tela.mostra_lista(relatorio)

    def exibir_relatorio_por_tipo_servico(self):
        if not self.__reservas:
            self.__tela.mostra_mensagem("Nenhuma reserva para gerar relatório de serviços.")
            return

        servicos_por_tipo = {}  # {tipo_servico: count, ...}

        for reserva in self.__reservas:
            for servico in reserva.servicos_quarto:
                tipo = servico.tipo_servico.capitalize()
                servicos_por_tipo[tipo] = servicos_por_tipo.get(tipo, 0) + 1

        if not servicos_por_tipo:
            self.__tela.mostra_mensagem("Nenhum serviço de quarto registrado nas reservas.")
            return

        relatorio = ["--- RELATÓRIO DE SERVIÇOS POR TIPO ---"]
        for tipo, count in servicos_por_tipo.items():
            relatorio.append(f"{tipo}: {count} vezes")

        self.__tela.mostra_lista(relatorio)

    @property
    def reservas(self) -> List[Reserva]:
        return self.__reservas