from typing import List, Optional
from app.models.user_model import User, PremiumUser
from app.repositories.user_repository import UserRepository
from fastapi import UploadFile


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        pass

    def add_user(
        self,
        user: User,
        premium: Optional[PremiumUser],
        avatar_file: Optional[UploadFile],
    ):
        if not user.userID or not user.username or not user.email or not user.style:
            raise ValueError("User ID, username, email, and style must be provided!")
        # Chỉ upload avatar nếu có file và file thực sự được chọn
        if avatar_file and getattr(avatar_file, "filename", None):
            if avatar_file.filename != "":
                img_url = self.repo.add_user_avatar(user, avatar_file)
                user.avatarPath = img_url
        # Add user to database
        self.repo.add_user_db(user, premium)

    def upgrade_user_to_premium(
        self, user: User, premium_user: PremiumUser, payment_verified: bool = False
    ):
        # Kiểm tra xác thực thanh toán trước khi nâng cấp
        if not payment_verified:
            raise ValueError(
                "Payment not verified! User cannot be upgraded to premium."
            )
        # Cập nhật thông tin premium cho user
        self.repo.upgrade_user_to_premium(user, premium_user)

    def update_user_avatar(self, userID: str, avatar_file: UploadFile):
        user = self.repo.get_user_by_id(userID)
        if not user:
            raise ValueError("User not found")
        # Upload file mới
        img_url = self.repo.add_user_avatar(user, avatar_file)
        # Update avatarPath cho user bằng update_db_service
        from firebase_admin import firestore as fs
        from firebase.firestore.firestore_micro_service.update import update_db_service

        db = fs.client()
        updater = update_db_service(
            db, "Users", {"userID": userID}, {"avatarPath": img_url}
        )
        updater.update()
        user.avatarPath = img_url
        return user

    def cancel_premium(self, userID: str):
        user = self.repo.get_user_by_id(userID)
        if not user:
            raise ValueError("User not found")
        # Update các trường premium về trạng thái user thường
        from firebase_admin import firestore as fs

        db = fs.client()
        doc_ref = db.collection("Users").document(userID)
        doc_ref.update(
            {
                "premium": False,
                "startdate": None,
                "enddate": None,
                "status": None,
            }
        )
        user.premium = False
        user_dict = user.model_dump()
        user_dict.update(
            {"premium": False, "startdate": None, "enddate": None, "status": None}
        )
        return user_dict
