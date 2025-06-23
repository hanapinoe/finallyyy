class firestore_initialize:
    def __init__(self, collection, document, subcollection, fields) -> None:
        # collection: tên collection cha (ví dụ: user1)
        # document: tên document (ví dụ: images)
        # subcollection: tên subcollection (ví dụ: file_id)
        # fields: dict metadata lưu vào Firestore
        self.collection = collection
        self.document = document
        self.subcollection = subcollection
        self.fields = fields




