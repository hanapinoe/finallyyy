from firebase.core.firebase_initialize import firebase_initialize


def firebase_service():
    """
    Hàm này khởi tạo và trả về đối tượng firebase_initialize với các tham số đã được cấu hình sẵn.
    Đường dẫn đến tệp tin chứng thực (key) và tên bucket được chỉ định cục bộ trong hàm.

    Trả về:
        firebase_initialize: Đối tượng firebase_initialize đã được cấu hình sẵn.
    """
    # Trả về đối tượng firebase_initialize đã cấu hình sẵn đường dẫn key và bucket
    certi = "E:\\own\\demo1\\firebase\\core\\thefirstflutterapp-firebase-adminsdk-fbsvc-1b0e4e5c42.json"
    buck = "thefirstflutterapp.firebasestorage.app"

    return firebase_initialize(certi, buck)
