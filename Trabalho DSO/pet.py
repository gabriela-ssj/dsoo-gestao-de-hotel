class Pet:
    def __init__(self, nome_pet: str, especie:str, quant_pet:int):
        self.__nome_pet = nome_pet
        self.__especie = especie
        self.__quant_pet = quant_pet
    
    @property
    def nome_pet(self):
        return self.__nome_pet
    
    @nome_pet.setter
    def nome_pet(self, nome_pet):
        self.__nome_pet = nome_pet

    @property
    def especie(self):
        return self.__especie
    
    @especie.setter
    def especie(self, especie):
        self.__especie = especie

    @property
    def quant_pet(self):
        return self.__quant_pet
    
    @quant_pet.setter
    def quant_pet(self, quant_pet):
        self.__quant_pet = quant_pet

    def exibir_infos_pet(self):
        print(f"Nome: {self.nome_pet};\n Espécie: {self.especie};\n Quantidade: {self.quant_pet}")
    
    def calcular_taxa_pet(self, taxa_por_animal: float) -> float:
        return self.__quant_pet * taxa_por_animal
    
    def __str__(self):
        return f"{self.quant_pet}X {self.especie}(s) chamado(s) {self.nome_pet}"
