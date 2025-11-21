from daos.dao import DAO
from entidades.pet import Pet


class PetDAO(DAO):
    def __init__(self):
        super().__init__('pets.pkl')

    def add(self, pet: Pet):
        if (
            pet is not None
            and isinstance(pet, Pet)
            and isinstance(pet.nome_pet, str)
        ):
            super().add(pet.nome_pet.lower(), pet)

    def update(self, pet: Pet):
        if (
            pet is not None
            and isinstance(pet, Pet)
            and isinstance(pet.nome_pet, str)
        ):
            super().update(pet.nome_pet.lower(), pet)

    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key.lower())

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key.lower())
