from fastapi import APIRouter, HTTPException
from app.models.drink_model import Drink
from app.repositories.drink_repository import DrinkRepository
from app.services.drink_service import DrinkService
from typing import List

# Tạo router cho các endpoint liên quan đến đồ uống
# Sử dụng APIRouter để tổ chức các route cho đồ uống
router = APIRouter(prefix="/drinks", tags=["drinks"])
service = DrinkService(DrinkRepository())

@router.post("/", response_model=Drink)
def add_drink(drink: Drink):
    """
    Thêm một đồ uống mới.
    """
    try:
        service.add_drink(drink, drink.imgPathStorage)
        return drink
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{drink_type}/{drink_id}", response_model=dict)
def delete_drink(drink_type: str, drink_id: str, imgPathStorage: str):
    """
    Xóa một đồ uống theo loại và ID, cần truyền thêm imgPathStorage từ client.
    """
    try:
        service.delete_drink(drink_type, drink_id, imgPathStorage)
        return {"message": "Drink deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
