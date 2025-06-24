from fastapi import APIRouter, UploadFile, File, Form, Query
from typing import Optional
from app.models.outfit_model import Outfit
from app.services.outfit_service import OutfitService
from app.repositories.outfit_repository import OutfitRepository

router = APIRouter(prefix="/outfits", tags=["Outfits"])
outfit_service = OutfitService(OutfitRepository())


@router.post("/add")
async def add_outfit(
    outfitID: str = Form(...),
    name: str = Form(...),
    type: str = Form(...),
    style: str = Form(...),
    image: UploadFile = File(...),
):
    # Lưu file tạm
    temp_path = f"temp_{image.filename}"
    with open(temp_path, "wb") as f:
        f.write(await image.read())
    # Gọi service để upload ảnh và lưu outfit
    outfit = Outfit(
        outfitID=outfitID,
        name=name,
        type=type,
        style=style,
        imgPathStorage="dummy",  # placeholder, sẽ được service cập nhật
    )
    outfit_service.add_outfit(outfit, imgPathLocal=temp_path)
    # Xóa file tạm
    import os

    try:
        os.remove(temp_path)
    except Exception:
        pass
    return {"success": True, "img_url": outfit.imgPathStorage}


@router.delete("/delete")
def delete_outfit(outfit_type: str = Query(...), outfit_id: str = Query(...)):
    success = outfit_service.delete_outfit(outfit_type, outfit_id)
    return {"success": success}


@router.get("/search")
def search_outfits(
    outfit_type: str = Query(...),
    search_option: str = Query(..., description="by_collection hoặc by_field"),
    outfit_id: Optional[str] = Query(None),
):
    result = outfit_service.search_outfits(outfit_type, search_option, outfit_id)
    return {"result": result}
