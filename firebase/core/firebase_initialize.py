import firebase_admin
from firebase_admin import credentials


class firebase_initialize:
    def __init__(self, certification, bucketName):
        # certification: Đường dẫn file json key Firebase
        # bucketName: Tên bucket Firebase Storage
        self.certification = certification
        self.bucketName = bucketName
        self._init_app()

    def _init_app(self):
        """
        Khởi tạo Firebase app với credentials và bucket nếu chưa có app nào.
        """
        if not firebase_admin._apps:
            cred = credentials.Certificate(self.certification)
            firebase_admin.initialize_app(cred, {"storageBucket": self.bucketName})

    def initialize(self):
        """
        Đảm bảo Firebase app đã được khởi tạo.
        """
        try:
            self._init_app()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
