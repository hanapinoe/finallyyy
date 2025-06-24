from typing import List, Optional
from app.models.outfit_model import Outfit
from app.repositories.outfit_repository import OutfitRepository
from fastapi import UploadFile


class OutfitService:
    def __init__(self, repo: OutfitRepository) -> None:
        self.repo = repo
        pass

    def add_outfit(self, outfit: Outfit, imgPathLocal: str) -> bool:
        if not (outfit.outfitID and outfit.name and outfit.type and outfit.style):
            raise ValueError("OutfitID, name, type, style are required")
        # Upload file và lấy đường dẫn thực tế trên Storage
        storage_path = self.repo.add_outfit_image(imgPathLocal)
        outfit.imgPathStorage = storage_path  # Lưu đúng đường dẫn Storage
        return self.repo.add_outfit_db(outfit)

    def delete_outfit(self, outfit_type: str, outfit_id: str) -> bool:
        if not outfit_type or not outfit_id:
            raise ValueError("Outfit type and ID are required")
        # Lấy metadata từ Firestore để lấy đúng imgPathStorage
        search_result = self.repo.search_outfits(outfit_type, "by_field", outfit_id)
        img_path_storage = None
        # Fix: robust type checking for search_result
        if isinstance(search_result, dict):
            result_list = search_result.get("result")
            if isinstance(result_list, list) and len(result_list) > 0:
                img_path_storage = result_list[0].get("imgPathStorage")
        elif isinstance(search_result, list) and len(search_result) > 0:
            img_path_storage = search_result[0].get("imgPathStorage")
        else:
            print(f"[DEBUG] Unexpected search_result type: {type(search_result)} value: {search_result}")
        deleted = self.repo.delete_outfit_db(outfit_type, outfit_id)
        if deleted and img_path_storage:
            return self.repo.delete_outfit_image(img_path_storage)
        return False

    def search_outfits(
        self,
        outfit_type: str,
        search_option: Optional[str],
        outfit_id: Optional[str] = None,
    ):
        if not outfit_type:
            raise ValueError("Outfit type is required")
        if not search_option:
            raise ValueError("Search option is required")
        result = self.repo.search_outfits(outfit_type, search_option, outfit_id)
        # Đảm bảo luôn trả về list hoặc dict, không phải str
        if isinstance(result, str):
            return {"success": False, "message": result}
        if not result:
            return {"success": False, "message": "No outfit found"}
        return {"success": True, "result": result}
