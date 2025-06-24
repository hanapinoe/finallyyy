from pydantic import BaseModel

# Outfit model representing clothing items
class Outfit(BaseModel):
    outfitID: str
    name: str
    type: str
    style: str
    imgPathLocal: str
    imgPathStorage: str
    history: bool
