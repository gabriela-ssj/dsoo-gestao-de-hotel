class Pet:
    def __init__(self, nome_pet: str, quant_pet:int):
        self.__nome_pet = nome_pet
        self.__quant_pet = quant_pet
    
    @property
    def nome_pet(self):
        return self.__nome_pet
    
    @nome_pet.setter
    def nome_pet(self, nome_pet):
        self.__nome_pet = nome_pet

    @property
    def quant_pet(self):
        return self.__quant_pet
    
    @quant_pet.setter
    def quant_pet(self, quant_pet):
        self.__quant_pet = quant_pet
