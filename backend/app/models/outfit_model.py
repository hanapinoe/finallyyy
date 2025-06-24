from pydantic import BaseModel
from typing import Optional


class Outfit(BaseModel):
    outfitID: str
    name: str
    type: str
    style: str
    imgPathStorage: (
        str  # Để đúng với luồng upload ảnh, luôn là str (URL), không Optional)
    )
