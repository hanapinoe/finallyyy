from firebase_admin import storage

class storage_initialize:
     def __init__(self, filePath, folderFirebaseStorage) -> None:
          # filePath: Đường dẫn file local
          # folderFirebaseStorage: Thư mục trên Firebase Storage
          self.filePath = filePath
          self.folderFirebaseStorage = folderFirebaseStorage

     def initialize_firebase_storage(self):
          # Chuẩn hóa đường dẫn và trả về blob Firebase Storage
          self.filePath = self.filePath.replace('\\', '/')
          fileName = self.filePath.split('/')[-1]
          fileFirebaseStoragePath = self.folderFirebaseStorage + '/' + fileName
          # Khởi tạo bucket và trả về blob
          bucket = storage.bucket()
          return bucket.blob(fileFirebaseStoragePath)