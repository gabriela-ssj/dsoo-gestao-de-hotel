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
from typing import List, Optional


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
            4: self.editar_reserva,
            5: self.adicionar_servico_a_reserva,
            6: self.adicionar_pet_a_reserva,
            7: self.calcular_valor_total_reserva,
            8: self.exibir_relatorio_por_hospede,
            9: self.exibir_relatorio_por_tipo_servico,
            0: self.retornar
        }

        while True:
            try:
                opcao = self.__tela.tela_opcoes()
                opcoes[opcao]()
                if opcao == 0:
                    break
            except ReservaException as e:
                self.__tela.mostra_mensagem(f"❌ Erro de reserva: {e}")
            except ValidacaoException as e:
                self.__tela.mostra_mensagem(f"⚠️ Erro de validação: {e}")
            except Exception as e:
                self.__tela.mostra_mensagem(f"🔥 Erro inesperado: {e}")

    def retornar(self):
        pass

    def fazer_reserva(self):
        try:
            dados_reserva = self.__tela.pega_dados_reserva()
            if not dados_reserva:
                raise ValidacaoException("Criação de reserva cancelada pelo usuário.")

            hospedes_encontrados = []
            for cpf in dados_reserva["cpfs_hospedes"]:
                hospede = self.__controlador_hospede.busca_hospede(cpf)
                if not hospede:
                    raise ReservaException(f"Hóspede com CPF {cpf} não encontrado.")
                hospedes_encontrados.append(hospede)

            if not hospedes_encontrados:
                raise ReservaException("Nenhum hóspede válido selecionado.")

            quartos_selecionados = []
            for numero_quarto in dados_reserva["numeros_quartos"]:
                quarto = self.__controlador_quarto.buscar_quarto(int(numero_quarto))
                if not quarto:
                    raise ReservaException(f"Quarto {numero_quarto} não existe.")

                if not quarto.disponibilidade:
                    raise ReservaException(f"Quarto {numero_quarto} está indisponível.")

                quartos_selecionados.append(quarto)

            nova_reserva = Reserva(
                hospedes=hospedes_encontrados,
                quartos=quartos_encontrados,
                data_checkin=checkin_data,
                data_checkout=checkout_data
            )

            conflicto = nova_reserva.reservar_quartos()
            if conflicto:  # se True = ERRO
                raise ReservaException("O quarto não pôde ser reservado (possível overlap).")

            self.__reservas.append(nova_reserva)
            self.__tela.mostra_mensagem(f"✅ Reserva ID {nova_reserva.id} criada com sucesso!")
            self.__tela.mostra_mensagem(nova_reserva.get_all_data())

        except (ValidacaoException, ReservaException):
            raise
        except Exception as e:
            raise ReservaException(f"Erro inesperado ao criar reserva: {e}")

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
    def listar_reservas(self):
        if not self.__reservas:
            self.__tela.mostra_mensagem("Nenhuma reserva cadastrada.")
            return
        lista_str = [str(reserva) for reserva in self.__reservas]
        self.__tela.mostra_lista_reservas(lista_str)

    def _selecionar_reserva(self, reserva_identificador=None) -> Optional[Reserva]:
        try:
            if not reserva_identificador:
                reserva_identificador = self.__tela.seleciona_reserva()

            if not reserva_identificador:
                raise ValidacaoException("Seleção de reserva cancelada.")

            try:
                reserva_id = int(reserva_identificador)
                for reserva in self.__reservas:
                    if reserva.id == reserva_id:
                        return reserva
            except ValueError:
                pass

            encontradas = [
                r for r in self.__reservas
                if r.hospedes and reserva_identificador.lower() in r.hospedes[0].nome.lower()
            ]

            if len(encontradas) == 1:
                return encontradas[0]
            if len(encontradas) > 1:
                raise ReservaException("Múltiplas reservas encontradas. Utilize o ID.")
            raise ReservaException("Reserva não encontrada.")

        except (ValidacaoException, ReservaException):
            raise
        except Exception as e:
            raise ReservaException(f"Erro inesperado ao buscar reserva: {e}")

    def cancelar_reserva(self):
        try:
            reserva = self._selecionar_reserva()
            confirmar = self.__tela.le_string("Confirmar cancelamento? (sim/nao): ")

            if confirmar.lower() != "sim":
                raise ValidacaoException("Cancelamento não confirmado.")

            reserva.liberar_quartos()
            self.__reservas.remove(reserva)
            self.__tela.mostra_mensagem("Reserva cancelada.")

        except (ValidacaoException, ReservaException):
            raise
        except Exception as e:
            raise ReservaException(f"Erro inesperado ao cancelar reserva: {e}")

    def editar_reserva(self):
        reserva = self._selecionar_reserva()
        dados = self.__tela.pega_dados_edicao()

        try:
            if not dados:
                raise ValidacaoException("Edição cancelada.")

            novos_quartos_obj = None

            if dados["limpar_quartos"]:
                novos_quartos_obj = []
            elif dados["novos_numeros_quartos"]:
                novos_quartos_obj = []
                for numero in dados["novos_numeros_quartos"]:
                    quarto = self.__controlador_quarto.buscar_quarto(int(numero))
                    if not quarto:
                        raise ReservaException(f"Quarto {numero} não existe.")
                    if not quarto.disponibilidade and quarto not in reserva.quartos:
                        raise ReservaException(f"Quarto {numero} indisponível.")
                    novos_quartos_obj.append(quarto)

            reserva.editar_reserva(
                nova_data_checkin=dados["nova_data_checkin"],
                nova_data_checkout=dados["nova_data_checkout"],
                novos_quartos=novos_quartos_obj
            )

            self.__tela.mostra_mensagem("Reserva editada com sucesso.")

        except (ValidacaoException, ReservaException):
            raise
        except Exception as e:
            raise ReservaException(f"Erro inesperado ao editar: {e}")

    def adicionar_servico_a_reserva(self):
        try:
            reserva = self._selecionar_reserva()
            dados = self.__tela.pega_dados_servico()
            if not dados:
                raise ValidacaoException("Operação cancelada.")

            quarto = None
            for q in reserva.quartos:
                if q.numero == int(dados["numero_quarto"]):
                    quarto = q
                    break
            if not quarto:
                raise ReservaException("Quarto não faz parte da reserva.")

            funcionario = self.__controlador_funcionario.buscar_funcionario(dados["cpf_funcionario"])
            if not funcionario:
                raise ReservaException("Funcionário não encontrado.")

            servico = ServicoDeQuarto(
                quarto=quarto,
                funcionario=funcionario,
                tipo_servico=dados["tipo_servico"],
                valor=dados["valor"]
            )

            reserva.adicionar_servico_quarto(servico)
            self.__tela.mostra_mensagem("Serviço adicionado.")

        except (ValidacaoException, ReservaException):
            raise
        except Exception as e:
            raise ReservaException(f"Erro inesperado ao adicionar serviço: {e}")

    def adicionar_pet_a_reserva(self):
        try:
            reserva = self._selecionar_reserva()

            hospede = self.__controlador_hospede.busca_hospede()
            nome_pet = self.__tela.le_string("Nome do pet: ")
            pet = hospede.busca_pet(nome_pet)

            reserva.adicionar_pet(pet)
            for quarto in reserva.quartos:
                quarto.adicionar_pet(pet)

            self.__tela.mostra_mensagem("Pet adicionado à reserva.")

        except (ValidacaoException, ReservaException):
            raise
        except Exception as e:
            raise ReservaException(f"Erro inesperado ao adicionar pet: {e}")

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
    def calcular_valor_total_reserva(self):
        reserva = self._selecionar_reserva()
        reserva.calcular_valor_total()
        self.__tela.mostra_mensagem(f"Valor total: R$ {reserva.valor_total:.2f}")

    def exibir_relatorio_por_hospede(self):
        if not self.__reservas:
            raise ValidacaoException("Nenhuma reserva cadastrada.")

        relatorio = []
        hospedes_reservas = {}

        reservas_do_hospede = []
        for reserva in self.__reservas:
            for hospede_na_reserva in reserva.hospedes:
                if hospede_na_reserva.cpf == cpf_hospede:
                    reservas_do_hospede.append(reserva.get_all_data())
                    break
            for hospede in reserva.hospedes:
                hospedes_reservas.setdefault(hospede.cpf, {"nome": hospede.nome, "ids": []})
                hospedes_reservas[hospede.cpf]["ids"].append(reserva.id)

        for cpf, info in hospedes_reservas.items():
            relatorio.append(
                f"{info['nome']} (CPF {cpf}) -> Reservas: {', '.join(map(str, info['ids']))}"
            )

        self.__tela.mostra_relatorio_hospede(cpf_hospede, reservas_do_hospede)

    def exibir_relatorio_por_tipo_servico(self):
        if not self.__reservas:
            raise ValidacaoException("Nenhuma reserva cadastrada.")

        servicos = {}
        for reserva in self.__reservas:
            for servico in reserva.servicos_quarto:
                tipo = servico.tipo_servico
                servicos[tipo] = servicos.get(tipo, 0) + 1

        if not servicos:
            self.__tela.mostra_mensagem("Nenhum serviço registrado.")
            return

        relatorio = [f"{k}: {v}x" for k, v in servicos.items()]
        self.__tela.mostra_lista(relatorio)

    @property
    def reservas(self) -> List[Reserva]:
        return self.__reservas
