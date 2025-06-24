from user_model import User
from outfit_model import Outfit

# Interactions with outfits by users
class interactUserWithOutfit(User, Outfit):
    User.userID
    Outfit.outfitID
    like: bool
    save: bool