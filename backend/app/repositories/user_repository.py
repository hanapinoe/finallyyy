from typing import List, Optional
from app.models.user_model import User, PremiumUser
from firebase.firestore.firestore_service import firestore_service
from firebase.storage.storage_service import storage_service
from firebase.core.firebase_service import firebase_service
from fastapi import UploadFile
import tempfile


class UserRepository:
    def __init__(self, collection: str = "Users"):
        self.collection = collection
        pass

    def add_user_db(self, user: User, premium: Optional[PremiumUser]):
        field = {
            "userID": user.userID,
            "username": user.username,
            "email": user.email,
            "avatarPath": user.avatarPath,
            "phone": user.phone,
            "address": user.address,
            "style": user.style,
            "premium": user.premium,
        }
        # Chỉ thêm các trường premium nếu có premium (nâng cấp)
        if user.premium and premium:
            field["startdate"] = premium.startdate
            field["enddate"] = premium.enddate
            field["status"] = premium.status
        firebase_service()
        from firebase_admin import firestore as fs

        db = fs.client()
        doc_ref = db.collection(self.collection).document(user.userID)
        doc_ref.set(field, merge=True)
        return True

    def add_user_avatar(self, user: User, avatar_file: UploadFile) -> str:
        firebase_service()
        # Lưu file tạm
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(avatar_file.file.read())
            tmp_path = tmp.name
        storage_obj = storage_service(tmp_path, f"{self.collection}/{user.userID}")
        img_url = storage_obj.upload_item()
        if not img_url:
            raise ValueError("Failed to upload avatar")
        return img_url

    def upgrade_user_to_premium(self, user: User, premium_user: PremiumUser):
        # Chỉ update các trường premium, không ghi đè các trường thường
        field = {
            "premium": True,
            "startdate": premium_user.startdate,
            "enddate": premium_user.enddate,
            "status": premium_user.status,
        }
        firebase_service()
        from firebase_admin import firestore as fs

        db = fs.client()
        doc_ref = db.collection(self.collection).document(user.userID)
        doc_ref.set(field, merge=True)
        return True

    def get_user_by_id(self, userID: str) -> Optional[User]:
        firebase_service()
        from firebase_admin import firestore as fs

        db = fs.client()
        doc_ref = db.collection(self.collection).document(userID)
        doc = doc_ref.get()
        if not doc.exists:
            return None
        user_data = doc.to_dict()
        if not user_data:
            return None
        return User(**user_data)
