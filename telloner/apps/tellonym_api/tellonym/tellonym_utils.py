from . import Tellonym as Client
from ..utils import error_dict
from .exceptions import *


def get_token(username, password):
    try:
        client = Client.Tellonym(username=username, password=password)
        return client.auth
    except RateLimitError:
        return error_dict("Slow down")
    except WrongCredentialsError:
        return error_dict("Incorrect username or password")


def get_username_from_token(token):
    client = Client.Tellonym(auth=token)
    try:
        user = client.get_profile()
    except Exception as err:
        return error_dict("Invalid token.")
    return user.username


def get_tells(token):
    client = Client.Tellonym(auth=token)
    try:
        tells = client.get_tells()
    except Exception:
        return error_dict("Invalid token.")
    return tells

