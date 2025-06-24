from typing import List, Optional
from app.models.outfit_model import Outfit
from firebase.firestore.firestore_service import firestore_service
from firebase.storage.storage_service import storage_service
from firebase.core.firebase_service import firebase_service


class OutfitRepository:
    def __init__(self, collection: str = "Outfits"):
        self.collection = collection
        pass

    def add_outfit_db(
        self,
        outfit: Outfit,
        include={"outfitID", "name", "type", "style", "imgPathLocal", "imgPathStorage"},
    ):
        firebase_service()
        firestore = firestore_service(
            collection=self.collection,
            document=outfit.type,
            subcollection=outfit.outfitID,
            field=outfit.model_dump(include=include),
        )
        return firestore.add_db()

    def add_outfit_image(self, imgPatchLocal: str) -> str:
        firebase_service()
        storage = storage_service(
            filePathLocal=imgPatchLocal, folderFirebaseStorage="outfits"
        )
        imgURL = storage.upload_item()
        if imgURL is None:
            raise ValueError("Failed to upload image to Firebase Storage")
        else:
            return imgURL

    def delete_outfit_db(self, outfit_type: str, outfit_id: str) -> bool:
        firebase_service()
        firestore = firestore_service(
            collection=self.collection,
            document=outfit_type,
            subcollection=outfit_id,
            field=None,
        )
        result = firestore.delete_db(outfit_id)
        if not result:
            print(
                f"[DEBUG] Không xóa được metadata Firestore: {self.collection}/{outfit_type}/{outfit_id}/{outfit_id}"
            )
        return result

    def delete_outfit_image(self, imgPathStorage: str) -> bool:
        firebase_service()
        storage = storage_service(filePathLocal=None, folderFirebaseStorage="outfits")
        result = storage.delete_item(imgPathStorage)
        if not result:
            print(f"[DEBUG] Không xóa được file trên Storage: {imgPathStorage}")
        return result

    def search_outfits(
        self, outfit_type: str, search_option: str, outfit_id: Optional[str]
    ):
        firebase_service()
        firestore = firestore_service(
            collection=self.collection,
            document=outfit_type,
            subcollection=None,
            field=None,
        )
        if search_option == "by_collection":
            return firestore.search_db(search_option, outfit_type)
        elif search_option == "by_field":
            if not outfit_id:
                raise ValueError("Outfit ID is required for field search")
            # Truyền đúng doc_name và subcollection_name cho search_by_field
            return firestore.search_db(
                search_option,
                doc_name=outfit_type,
                subcollection_name=outfit_id,
                field_input={"outfitID": outfit_id},
            )
        else:
            raise ValueError(
                "Invalid search option. Use 'by_collection' or 'by_field'."
            )
