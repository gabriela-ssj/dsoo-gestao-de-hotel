class Pet:
    def __init__(self, nome_pet: str, especie: str, quant_pet: int = 1):
        self.__nome_pet = nome_pet
        self.__especie = especie
        self.__quant_pet = quant_pet

    @property
    def nome_pet(self) -> str:
        return self.__nome_pet

    @nome_pet.setter
    def nome_pet(self, nome_pet: str):
        self.__nome_pet = nome_pet

    @property
    def especie(self) -> str:
        return self.__especie

    @especie.setter
    def especie(self, especie: str):
        self.__especie = especie

    @property
    def quant_pet(self) -> int:
        return self.__quant_pet

    @quant_pet.setter
    def quant_pet(self, quantidade: int):
        if quantidade < 1:
            raise ValueError("A quantidade de pets deve ser pelo menos 1.")
        self.__quant_pet = quantidade

    def calcular_taxa_pet(self, taxa_por_animal: float) -> float:
        return self.__quant_pet * taxa_por_animal

    def exibir_infos_pet(self) -> str:
        return (
            f"Nome: {self.nome_pet}\n"
            f"Espécie: {self.especie}\n"
            f"Quantidade: {self.quant_pet}"
        )

    def __str__(self) -> str:
        return f"{self.quant_pet}x {self.especie}(s) chamado(s) {self.nome_pet}"
    