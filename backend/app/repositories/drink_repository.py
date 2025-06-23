from typing import List, Optional
from app.models.drink_model import Drink
from firebase.firestore.firestore_service import firestore_service
from firebase.storage.storage_service import storage_service
from firebase.core.firebase_service import firebase_service


class DrinkRepository:
    def __init__(self, collection: str = "drinks"):
        self.collection = collection
        pass

    # Thêm một đồ uống mới vào Firestore
    # include: các trường cần lưu vào Firestore, mặc định là {"name", "price", "imgPathLocal", "imgPathStorage"}
    def add_drink_db(self, drink: Drink, include={"name", "price", "imgPathLocal", "imgPathStorage"}):
        firebase_service()  # Đảm bảo Firebase app đã được khởi tạo
        firestore = firestore_service(
            collection=self.collection,
            document=drink.type,
            subcollection=drink.id,
            field=drink.model_dump(include=include),
        )

        return firestore.add_db()

    # Xóa một đồ uống theo loại và ID
    # drink_type: loại đồ uống (ví dụ: "coffee", "tea")
    def delete_drink_db(self, drink_type: str, drink_id: str) -> bool:
        firebase_service()  # Đảm bảo Firebase app đã được khởi tạo
        firestore = firestore_service(
            collection=self.collection,
            document=drink_type,
            subcollection=drink_id,
            field=None,
        )
        return firestore.delete_db(drink_id)

    # Add image path to Firestore
    ## imgPatchLocal: local path of the image
    ## imgPathStorage: path in Firebase Storage where the image is stored
    def add_drink_image(self, imgPatchLocal: str, imgPathStorage: str) -> str:
        firebase_service()  # Đảm bảo Firebase app đã được khởi tạo
        storage = storage_service(
            filePath=imgPatchLocal, folderFirebaseStorage="drinks"
        )
        imgURL = storage.upload_item()
        if imgURL is None:
            raise ValueError("Failed to upload image to Firebase Storage")
        else:
            return imgURL

    # Delete image path from Firestore
    ## imgPathStorage: path in Firebase Storage where the image is stored
    def delete_drink_image(self, imgPathStorage: str) -> bool:
        firebase_service()  # Đảm bảo Firebase app đã được khởi tạo
        storage = storage_service(filePath=None, folderFirebaseStorage="drinks")
        return storage.delete_item(imgPathStorage)
    
    # Lấy tất cả đồ uống từ Firestore
    # def get_all(self) -> List[Drink]:
    #     print("DEBUG: get_all called")
    #     firebase_service()  # Đảm bảo Firebase app đã được khởi tạo
    #     from firebase_admin import firestore as fs
    #     db = fs.client()
    #     drinks: List[Drink] = []
    #     # Lấy tất cả document trong collection drinks
    #     for doc in db.collection(self.collection).stream():
    #         print(f"DEBUG parent doc: {doc.id}")
    #         # Duyệt qua tất cả subcollection của từng document
    #         for subcol in doc.reference.collections():
    #             print(f"DEBUG subcollection: {subcol.id}")
    #             for subdoc in subcol.stream():
    #                 data = subdoc.to_dict()
    #                 print(f"DEBUG subdoc: {subdoc.id} => {data}")
    #                 # Bổ sung id, type nếu thiếu
    #                 if "id" not in data:
    #                     data["id"] = subdoc.id
    #                 if "type" not in data:
    #                     data["type"] = doc.id
    #                 try:
    #                     drinks.append(Drink.model_validate(data))
    #                 except Exception as e:
    #                     print(f"Model validate error: {e}, data: {data}")
    #     return drinks