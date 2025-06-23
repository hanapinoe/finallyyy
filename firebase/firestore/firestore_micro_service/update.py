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

    def update(self):
        """
        Tìm các document phù hợp với data_old rồi update theo data_new
        """
        search_service = search_db_service(
            self.db, self.collection_input, self.data_old
        )
        collection_paths = search_service.search_by_field()
        if collection_paths:
            updated = False
            for collection_path in collection_paths:
                collection_path_split = collection_path.strip().split("/")
                if len(collection_path_split) == 3:
                    collection = self.collection_input
                    document = collection_path_split[0]
                    subcol = collection_path_split[1]
                    subdoc = collection_path_split[2]

                    doc_ref = (
                        self.db.collection(collection)
                        .document(document)
                        .collection(subcol)
                        .document(subdoc)
                    )
                    try:
                        doc_ref.update(self.data_new)
                        print(f"Update successfully: {collection_path}")
                        updated = True
                    except Exception as e:
                        print(f"Error updating {collection_path}: {e}")
            if updated:
                return True
            else:
                print("No documents updated!")
                return False
        else:
            print("Can not find documents to update!")
            return False
