from firebase_admin import firestore
from firebase.firestore.firestore_initialize import (
    firestore_initialize,
)  # Khởi tạo base cho Firestore
from firebase.firestore.firestore_micro_service.search import (
    search_db_service,
)  # Service tìm kiếm
from firebase.firestore.firestore_micro_service.update import (
    update_db_service,
)  # Service cập nhật


class firestore_service(firestore_initialize):
    def __init__(self, collection, document, subcollection, field) -> None:
        # Khởi tạo service Firestore, truyền vào tên collection cha, document, subcollection và fields
        super().__init__(collection, document, subcollection, field)
        self.db = firestore.client()

    def add_db(self):
        """
        Thêm metadata vào Firestore theo cấu trúc:
            collection (user1) / document (images) / subcollection (file_id) / document (file_id)
        """
        try:
            # Sử dụng subcollection là tên file (không đuôi), document ID cũng là tên file (không đuôi)
            self.db.collection(self.collection).document(self.document).collection(
                self.subcollection
            ).document(self.subcollection).set(self.fields)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def search_db(
        self, search_option, doc_name=None, subcollection_name=None, field_input=None
    ):
        """
        Gọi các hàm search (by_collection, by_field) từ search_db_service
        """
        search_service = search_db_service(self.db, self.collection, field_input)
        result = None
        if search_option == "by_collection":
            # Nếu doc_name là None thì truyền chuỗi rỗng để tránh lỗi type
            doc_name = doc_name or ""
            result = search_service.search_by_collection(doc_name)
        elif search_option == "by_field":
            if doc_name is None or subcollection_name is None:
                raise ValueError(
                    "doc_name và subcollection_name là bắt buộc cho by_field"
                )
            result = search_service.search_by_field(doc_name, subcollection_name)
        return result

    # def update_db(self, collection_input, data_old, data_new):
    #     """
    #     Gọi hàm update từ update_db_service
    #     """
    #     update_service = update_db_service(self.db, collection_input, data_old, data_new)
    #     return update_service.update()

    def delete_db(self, file_id):
        """
        Xóa metadata của 1 file (subcollection + document) trong Firestore.
        """
        try:
            doc_ref = (
                self.db.collection(self.collection)
                .document(self.document)
                .collection(file_id)
                .document(file_id)
            )
            doc_ref.delete()
            print(
                f"Đã xóa metadata Firestore: {self.collection}/{self.document}/{file_id}/{file_id}"
            )
            return True
        except Exception as e:
            print(f"Lỗi khi xóa metadata Firestore: {e}")
            return False

    def get_info(self, collection_input):
        # Chưa triển khai
        pass

    def list_all_data(self):
        """
        Duyệt toàn bộ collection 'drinks' và các subcollection bên trong, trả về list chứa metadata của tất cả đồ uống.
        """
        result = []
        print("DEBUG: Danh sách collection top-level:")
        for col in self.db.collections():
            print("  -", col.id)
        drinks_col = self.db.collection("drinks")
        print("DEBUG: Danh sách document trong 'drinks':")
        for doc in drinks_col.stream():
            print("  -", doc.id)
            doc_id = doc.id  # ví dụ: Coffee
            # Duyệt các subcollection bên trong mỗi document
            for subcol in doc.reference.collections():
                print("    Subcollection:", subcol.id)
                subcol_id = subcol.id  # ví dụ: 2
                for subdoc in subcol.stream():
                    print("      Subdoc:", subdoc.id, subdoc.to_dict())
                    subdoc_id = subdoc.id  # ví dụ: 2
                    data = subdoc.to_dict()
                    result.append(
                        {
                            "path": f"drinks/{doc_id}/{subcol_id}/{subdoc_id}",
                            "data": data,
                        }
                    )
        return result
