from .models import TellonymUser
from .utils import hash_text, error_dict


def get_user(username, token):
    hashed_username = hash_text(username)
    hashed_token = hash_text(token)
    try:
        user = TellonymUser.objects.get(hashed_username=hashed_username, hashed_token=hashed_token)
    except TellonymUser.DoesNotExist:
        return error_dict("User does not exist or bad token.")
    return user

