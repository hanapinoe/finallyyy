from typing import List
from app.models.drink_model import Drink
from app.repositories.drink_repository import DrinkRepository


class DrinkService:
    def __init__(self, repo: DrinkRepository):
        self.repo = repo

    def add_drink(self, drink: Drink, storagePath: str) -> None:
        if (
            not drink.id
            or not drink.name
            or not drink.type
            or not drink.price
            or not drink.imgPathLocal
        ):
            raise ValueError("All fields must be provided!")
        imgURL = self.repo.add_drink_image(drink.imgPathLocal, storagePath)
        drink.imgPathStorage = imgURL
        self.repo.add_drink_db(drink)

    def delete_drink(self, drink_type: str, drink_id: str, imgPathStorage: str):
        if not drink_type or not drink_id:
            raise ValueError("Drink type and ID must be provided!")
        if not self.repo.delete_drink_db(drink_type, drink_id):
            raise ValueError("Failed to delete drink from repository!")
        if imgPathStorage:
            self.repo.delete_drink_image(imgPathStorage)
