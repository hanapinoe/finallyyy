from firebase_admin import storage

class storage_initialize:
     def __init__(self, filePathLocal, folderFirebaseStorage) -> None:
          # filePathLocal: Đường dẫn file local
          # folderFirebaseStorage: Thư mục trên Firebase Storage
          self.filePathLocal = filePathLocal
          self.folderFirebaseStorage = folderFirebaseStorage

     def initialize_firebase_storage(self):
          # Chuẩn hóa đường dẫn và trả về blob Firebase Storage
          self.filePathLocal = self.filePathLocal.replace('\\', '/')
          fileName = self.filePathLocal.split('/')[-1]
          fileFirebaseStoragePath = self.folderFirebaseStorage + '/' + fileName
          # Khởi tạo bucket và trả về blob
          bucket = storage.bucket()
          return bucket.blob(fileFirebaseStoragePath)