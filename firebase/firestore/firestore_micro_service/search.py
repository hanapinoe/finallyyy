from firebase_admin import firestore


class search_db_service:
    def __init__(self, db, collection_input, field_input=None) -> None:
        # db: Đối tượng Firestore client
        # collection_input: Tên collection cha cần tìm kiếm (ví dụ: "user1")
        # field_input: dict chứa field và giá trị cần tìm, ví dụ {'field_name': 'value'}
        self.db = db
        self.collection_input = collection_input
        self.field_input = field_input

    def search_by_collection(self, doc_name: str = ""):
        """
        Lấy tất cả subcollection (outfit id) và document bên trong của document cha (doc_name).
        Nếu không truyền doc_name hoặc doc_name rỗng, sẽ lấy tất cả document ở collection cha.
        """
        if self.collection_input is not None:
            try:
                if doc_name:
                    doc_ref = self.db.collection(self.collection_input).document(
                        doc_name
                    )
                    subcollections = doc_ref.collections()
                    all_docs = []
                    for subcol in subcollections:
                        for subdoc in subcol.stream():
                            data = subdoc.to_dict()
                            all_docs.append(data)
                    if not all_docs:
                        print("No documents found in subcollections!")
                    return all_docs
                else:
                    collections_ref = self.db.collection(self.collection_input)
                    docs = collections_ref.stream()
                    all_docs = []
                    for doc in docs:
                        all_docs.append(doc.to_dict())
                    if not all_docs:
                        print("Collection is empty!")
                    return all_docs
            except Exception as e:
                print(f"Error: {e}")
                return []
        else:
            return []

    # def search_by_field(self):
    #     """
    #     Tìm kiếm và in ra tất cả subdocument trong mọi subcollection của document 'images'
    #     bên trong collection cha (ví dụ: 'user1'), thỏa mãn điều kiện field_input.
    #     Trả về list các đường dẫn subdocument tìm được.

    #     Cấu trúc Firestore mong đợi:
    #         user1 (collection)
    #             images (document)
    #                 <file_id> (subcollection)
    #                     <file_id> (document chứa metadata)
    #     """
    #     if self.collection_input is not None and self.field_input is not None:
    #         try:
    #             # Lấy tên field và giá trị cần tìm
    #             field_name, value = next(iter(self.field_input.items()))
    #             # Truy cập document 'images' trong collection cha (ví dụ: 'user1')
    #             doc_ref = self.db.collection(self.collection_input).document("images")
    #             subcollections = doc_ref.collections()  # Lấy tất cả subcollection (tên là file_id)
    #             found_paths = []
    #             for subcol in subcollections:
    #                 for subdoc in subcol.stream():
    #                     data = subdoc.to_dict()
    #                     # So sánh giá trị field (dùng str để tránh lỗi kiểu dữ liệu)
    #                     if str(data.get(field_name)) == str(value):
    #                         file_path = f"{self.collection_input}/images/{subcol.id}/{subdoc.id}"
    #                         print(f"Tìm thấy: {file_path} => {data}")
    #                         found_paths.append(file_path)
    #             if not found_paths:
    #                 print("Không tìm thấy subdocument nào phù hợp!")
    #             return found_paths
    #         except Exception as e:
    #             print(f"Lỗi: {e}")
    #             return []
    #     else:
    #         print("collection_input hoặc field_input bị thiếu!")
    #         return []

    def search_by_field(self, doc_name: str, subcollection_name: str):
        """
        Tìm kiếm document theo field trong subcollection của document cha.
        doc_name: document cha (ví dụ: 'áo')
        subcollection_name: subcollection (ví dụ: 'outfit 2')
        """
        if self.collection_input is not None and self.field_input is not None:
            try:
                field_name, value = next(iter(self.field_input.items()))
                doc_ref = self.db.collection(self.collection_input).document(doc_name)
                subcol_ref = doc_ref.collection(subcollection_name)
                found_docs = []
                for subdoc in subcol_ref.stream():
                    data = subdoc.to_dict()
                    if str(data.get(field_name)) == str(value):
                        found_docs.append(data)
                if not found_docs:
                    print("Không tìm thấy document nào phù hợp!")
                return found_docs
            except Exception as e:
                print(f"Lỗi: {e}")
                return []
        else:
            print("collection_input hoặc field_input bị thiếu!")
            return []
