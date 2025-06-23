from firebase_admin import firestore

class search_db_service:
    def __init__(self, db, collection_input, field_input=None) -> None:
        # db: Đối tượng Firestore client
        # collection_input: Tên collection cha cần tìm kiếm (ví dụ: "user1")
        # field_input: dict chứa field và giá trị cần tìm, ví dụ {'field_name': 'value'}
        self.db = db
        self.collection_input = collection_input
        self.field_input = field_input

    def search_by_collection(self):
        """
        In ra tất cả document trong collection cha.
        Nếu collection không có document, in ra thông báo.
        """
        if self.collection_input is not None:
            try:
                collections_ref = self.db.collection(self.collection_input)
                docs = collections_ref.stream()
                found = False
                for doc in docs:
                    print(f"{doc.id} => {doc.to_dict()}")  # In ra id và dữ liệu của từng document
                    found = True
                if not found:
                    print("Collection is empty!")  # Nếu không có document nào
            except Exception as e:
                print(f"Error: {e}")  # Xử lý ngoại lệ
            return True
        else:
            return False

    def search_by_field(self):
        """
        Tìm kiếm và in ra tất cả subdocument trong mọi subcollection của document 'images'
        bên trong collection cha (ví dụ: 'user1'), thỏa mãn điều kiện field_input.
        Trả về list các đường dẫn subdocument tìm được.
        
        Cấu trúc Firestore mong đợi:
            user1 (collection)
                images (document)
                    <file_id> (subcollection)
                        <file_id> (document chứa metadata)
        """
        if self.collection_input is not None and self.field_input is not None:
            try:
                # Lấy tên field và giá trị cần tìm
                field_name, value = next(iter(self.field_input.items()))
                # Truy cập document 'images' trong collection cha (ví dụ: 'user1')
                doc_ref = self.db.collection(self.collection_input).document("images")
                subcollections = doc_ref.collections()  # Lấy tất cả subcollection (tên là file_id)
                found_paths = []
                for subcol in subcollections:
                    for subdoc in subcol.stream():
                        data = subdoc.to_dict()
                        # So sánh giá trị field (dùng str để tránh lỗi kiểu dữ liệu)
                        if str(data.get(field_name)) == str(value):
                            file_path = f"{self.collection_input}/images/{subcol.id}/{subdoc.id}"
                            print(f"Tìm thấy: {file_path} => {data}")
                            found_paths.append(file_path)
                if not found_paths:
                    print("Không tìm thấy subdocument nào phù hợp!")
                return found_paths
            except Exception as e:
                print(f"Lỗi: {e}")
                return []
        else:
            print("collection_input hoặc field_input bị thiếu!")
            return []