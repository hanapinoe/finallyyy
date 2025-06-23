from firebase.storage.storage_initialize import storage_initialize

class storage_service(storage_initialize):
    def __init__(self, filePath, folderFirebaseStorage) -> None:
        # Kế thừa storage_initialize, truyền vào đường dẫn file và thư mục Storage
        super().__init__(filePath, folderFirebaseStorage)
    
    def upload_item(self):
        # Upload file lên Firebase Storage
        blob = super().initialize_firebase_storage()
        try:
            blob.upload_from_filename(self.filePath)
            blob.make_public()  # Tùy chọn: làm cho file có thể truy cập công khai
            return blob.public_url  # Trả về URL công khai của file
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def delete_item(self, storage_path):
        """
        Xóa file trên Firebase Storage theo đường dẫn (storage_path).
        """
        try:
            from firebase_admin import storage
            bucket = storage.bucket()
            blob = bucket.blob(storage_path)
            blob.delete()
            print(f"Đã xóa file trên Storage: {storage_path}")
            return True
        except Exception as e:
            print(f"Lỗi khi xóa file trên Storage: {e}")
            return False