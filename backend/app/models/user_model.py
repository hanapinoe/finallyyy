from pydantic import BaseModel


# User model representing a user in the system
class User(BaseModel):
    userID: str
    username: str
    email: str
    phone: None | str = None
    address: None | str = None
    avatarPath: str | None = None  # Storage path for user avatar image, không bắt buộc
    style: str
    premium: bool


# PremiumUser model extending User with additional fields for premium users
class PremiumUser(User):
    premium: bool = True
    startdate: str
    enddate: str
    status: str
