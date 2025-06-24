# from typing import List, Optional
# from app.models.outfit_model import Outfit
# from firebase.firestore.firestore_service import firestore_service
# from firebase.storage.storage_service import storage_service
# from firebase.core.firebase_service import firebase_service

# class OutfitRepository:
#     def __init__(self, collection: str = "Outfits"):
#         self.collection = collection
#         pass

#     def add_outfit_db(
#         self,
#         outfit: Outfit,
#         include={"outfitID", "name", "type", "style", "imgPathLocal", "imgPathStorage"},
#     ):
#         firebase_service()
#         firestore = firestore_service(
#             collection=self.collection,
#             document=outfit.type,
#             subcollection=outfit.outfitID,
#             field=outfit.model_dump(include=include),
#         )
#         return firestore.add_db()
    
#     def add_outfit_image(self, imgPatchLocal: str, imgPathStorage: str) -> str:
#         firebase_service()
#         storage = storage_service(
#             filePath=imgPatchLocal, folderFirebaseStorage="drinks"
#         )
#         imgURL = storage.upload_item()
#         if imgURL is None:
#             raise ValueError("Failed to upload image to Firebase Storage")
#         else:
#             return imgURL

#     def delete_outfit_db(self, outfit_type: str, outfit_id: str) -> bool:
#         firebase_service()
#         firestore = firestore_service(
#             collection=self.collection,
#             document=outfit_type,
#             subcollection=outfit_id,
#             field=None,
#         )
#         return firestore.delete_db(outfit_id)

#     def delete_outfit_image(self, imgPathStorage: str) -> bool:
#         firebase_service()
#         storage = storage_service(filePath=None, folderFirebaseStorage="drinks")
#         return storage.delete_item(imgPathStorage)
