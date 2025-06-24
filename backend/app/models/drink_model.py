from pydantic import BaseModel

class Drink(BaseModel):
    id : str
    name : str
    type : str
    price : float
    imgPathLocal: str
    imgPathStorage: str

