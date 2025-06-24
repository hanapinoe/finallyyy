from fastapi import APIRouter, HTTPException, UploadFile, Form, File
from app.models.user_model import User, PremiumUser
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from typing import List, Optional

# Tạo router cho các endpoint liên quan đến người dùng
# Sử dụng APIRouter để tổ chức các route cho người dùng
router = APIRouter(prefix="/Users", tags=["Users"])
service = UserService(UserRepository())


@router.post("/", response_model=User)
def add_user(
    userID: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    address: str = Form(None),
    style: str = Form(...),
    avatar_file: Optional[UploadFile] = File(None),  # Không bắt buộc
):
    """
    Thêm một người dùng mới.
    """
    try:
        print(
            f"[DEBUG] add_user: userID={userID}, username={username}, email={email}, phone={phone}, address={address}, style={style}, avatar_file={avatar_file}"
        )
        user = User(
            userID=userID,
            username=username,
            email=email,
            phone=phone,
            address=address,
            avatarPath="",  # Để chuỗi rỗng thay vì None
            style=style,
            premium=False,  # Luôn mặc định là False khi tạo user mới
        )
        # Nếu không có file hoặc file rỗng thì không upload avatar, không làm gì cả
        if (
            avatar_file
            and getattr(avatar_file, "filename", None)
            and avatar_file.filename != ""
        ):
            print(f"[DEBUG] add_user: avatar_file.filename={avatar_file.filename}")
            service.add_user(user, None, avatar_file)
        else:
            print(f"[DEBUG] add_user: No avatar file uploaded")
            service.add_user(user, None, None)
        print(f"[DEBUG] add_user: user created: {user}")
        return user
    except ValueError as e:
        print(f"[DEBUG] add_user: error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upgrade-premium", response_model=User)
def upgrade_premium(
    userID: str = Form(...),
    startdate: str = Form(...),
    enddate: str = Form(...),
    status: str = Form(...),
):
    """
    Nâng cấp user lên premium.
    """
    try:
        print(
            f"[DEBUG] upgrade_premium: userID={userID}, startdate={startdate}, enddate={enddate}, status={status}"
        )
        # Lấy user từ DB
        user = service.repo.get_user_by_id(userID)
        print(f"[DEBUG] upgrade_premium: user from DB: {user}")
        if not user:
            print(f"[DEBUG] upgrade_premium: User not found")
            raise ValueError("User not found")
        # Tạo PremiumUser từ dict thay vì truyền từng field để tránh lỗi lint và đảm bảo an toàn
        user_dict = user.model_dump()
        user_dict.update(
            {
                "premium": True,
                "startdate": startdate,
                "enddate": enddate,
                "status": status,
            }
        )
        premium_user = PremiumUser(**user_dict)
        print(f"[DEBUG] upgrade_premium: premium_user={premium_user}")
        # Thêm tham số payment_verified, mặc định False để không cho phép nâng cấp nếu chưa xác thực thanh toán
        service.upgrade_user_to_premium(user, premium_user, payment_verified=True)
        print(f"[DEBUG] upgrade_premium: user upgraded to premium")
        return premium_user
    except ValueError as e:
        print(f"[DEBUG] upgrade_premium: error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update-avatar", response_model=User)
def update_avatar(
    userID: str = Form(...),
    avatar_file: UploadFile = File(...),
):
    """
    Cập nhật ảnh đại diện cho user.
    """
    try:
        user = service.update_user_avatar(userID, avatar_file)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/cancel-premium", response_model=User)
def cancel_premium(
    userID: str = Form(...),
):
    """
    Hủy gói premium, chuyển user về trạng thái thường.
    """
    try:
        user = service.cancel_premium(userID)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
