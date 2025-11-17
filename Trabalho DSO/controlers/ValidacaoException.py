
class ValidacaoException(Exception):
    """Exceções e validadores reutilizáveis para regras de negócio."""

    def __init__(self, mensagem):
        super().__init__(mensagem)


    @staticmethod
    def se_none(valor, mensagem):
        if valor is None:
            raise ValidacaoException(mensagem)

    @staticmethod
    def se_vazio(lista, mensagem):
        if not lista:
            raise ValidacaoException(mensagem)

    @staticmethod
    def validar_booleano(condicao, mensagem):
        if condicao:
            raise ValidacaoException(mensagem)

    @staticmethod
    def validar_cpf_unico(lista, cpf):
        for f in lista:
            if f.cpf == cpf:
                raise ValidacaoException(f"CPF {cpf} já está cadastrado.")

    @staticmethod
    def validar_idade_valida(idade):
        if idade <= 0 or idade > 120:
            raise ValidacaoException("Idade inválida. Digite um número entre 1 e 120.")

    @staticmethod
    def validar_campo_vazio(campo, nome):
        if campo.strip() == "":
            raise ValidacaoException(f"O campo '{nome}' não pode estar vazio.")

    @staticmethod
    def validar_email(email):
        if "@" not in email or "." not in email:
            raise ValidacaoException("Email inválido.")

    @staticmethod
    def validar_salario_valido(salario):
        if not isinstance(salario, (int, float)) or salario < 0:
            raise ValidacaoException("Salário inválido. Digite um número positivo.")