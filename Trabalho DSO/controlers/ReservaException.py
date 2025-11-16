
class ReservaException(Exception):
    """Erros de regra de negócio da reserva."""

    @staticmethod
    def quarto_indisponivel(numero):
        raise ReservaException(f"Quarto {numero} não está disponível para reserva.")

    @staticmethod
    def quarto_invalido(numero):
        raise ReservaException(f"Quarto {numero} não foi encontrado.")

    @staticmethod
    def hospede_invalido(cpf):
        raise ReservaException(f"Hóspede com CPF {cpf} não foi encontrado.")

    @staticmethod
    def pet_nao_permitido(quarto, pet):
        raise ReservaException(
            f"O quarto {quarto.numero} não aceita pets. Pet '{pet.nome_pet}' não pode ser alocado."
        )

    @staticmethod
    def reserva_sobreposta(quarto):
        raise ReservaException(
            f"O quarto {quarto.numero} já está reservado no período selecionado."
        )

    @staticmethod
    def servico_invalido(motivo):
        raise ReservaException(f"Serviço de quarto inválido: {motivo}")

    @staticmethod
    def reserva_inexistente(identificador):
        raise ReservaException(f"Nenhuma reserva encontrada para '{identificador}'.")
