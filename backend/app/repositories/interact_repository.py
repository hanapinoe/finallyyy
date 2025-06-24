from typing import List, Optional
from app.models.interact_model import interactUserWithOutfit
from firebase.firestore.firestore_service import firestore_service

class InteractRepository:
    def __init__(self, collection: str = "Interactions"):
        self.collection = collection
        pass

    def add_interact_db(self, interact: interactUserWithOutfit):
        if interact.like is None and interact.save is None:
            return None  # Không ghi nhận nếu không có tương tác
        if interact.like is None:
            include = {"save": True}
        elif interact.save is None:
            include = {"like": True}
        else:
            include = {"like": True, "save": True}
        service = firestore_service(
            collection=self.collection,
            document=interact.userID,
            subcollection=interact.outfitID,
            field=interact.model_dump(include=include),
        )
        service.add_db()
        return service

    def delete_interact_db(
        self, user_id: str, outfit_id: str, interact_type: str
    ) -> bool:
        if (
            user_id is None
            or outfit_id is None
            or interact_type not in ("like", "save")
        ):
            return False
        # Chỉ cập nhật trạng thái like/save về False, không xóa toàn bộ tương tác
        field = {interact_type: False}
        service = firestore_service(
            collection=self.collection,
            document=user_id,
            subcollection=outfit_id,
            field=field,
        )
        return service.add_db()  # Cập nhật trạng thái tương tác
