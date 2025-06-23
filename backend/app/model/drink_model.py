from pydantic import BaseModel

class Drink(BaseModel):
    id : str
    name : str
    type : str
    price : float
    imgPathLocal: str
    imgPathStorage: str

class Food(BaseModel):
    id : str
    name : str
    type : str
    price : float
    imgPathLocal: str
    imgPathStorage: str

class User(BaseModel):
    id: str
    username: str
    email: str
    phone: str
    address: str

class Order(BaseModel):
    id: str
    userId: str
    drinkId: str
    foodId: str
    quantity: int
    totalPrice: float
    status: str  # e.g., "pending", "completed", "cancelled"
    orderDate: str  # ISO format date string

