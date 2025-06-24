from firebase_admin import firestore
from firebase.firestore.firestore_micro_service.search import search_db_service


class update_db_service:
    def __init__(self, db, collection_input, data_old, data_new) -> None:
        # db: Firestore client
        # collection_input: collection cha (user1)
        # data_old: dict điều kiện tìm kiếm
        # data_new: dict dữ liệu mới để update
        self.db = db
        self.collection_input = collection_input
        self.data_old = data_old
        self.data_new = data_new

    def update(self, doc_name, subcollection_name):
        """
        Tìm các document phù hợp với data_old rồi update theo data_new
        """
        search_service = search_db_service(
            self.db, self.collection_input, self.data_old
        )
        found_docs = search_service.search_by_field(doc_name, subcollection_name)
        if found_docs:
            updated = False
            for doc in found_docs:
                doc_ref = (
                    self.db.collection(self.collection_input)
                    .document(doc_name)
                    .collection(subcollection_name)
                    .document(doc.get("outfitID"))  # hoặc key định danh phù hợp
                )
                try:
                    doc_ref.update(self.data_new)
                    print(f"Update successfully: {doc.get('outfitID')}")
                    updated = True
                except Exception as e:
                    print(f"Error updating {doc.get('outfitID')}: {e}")
            if updated:
                return True
            else:
                print("No documents updated!")
                return False
        else:
            print("Can not find documents to update!")
            return False
