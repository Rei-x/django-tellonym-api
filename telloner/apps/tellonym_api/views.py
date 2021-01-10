from .models import TellonymUser
from .tellonym import tellonym_utils
from .utils import hash_text
from .authentication import get_user
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, Http404
import jsonpickle


def get_username_from_token():
    pass


def index(request):

    try:
        username = request.headers['Username']
        token = request.headers['Authorization']
    except Exception:
        return HttpResponse(status=401)

    user = get_user(username, token)

    if isinstance(user, TellonymUser):
        tells = tellonym_utils.get_tells(token)
        user.add_tells(tells)
        array = jsonpickle.encode(tells, unpicklable=False)
        return HttpResponse(array, content_type="application/json")
    raise Http404


def login(request):
    username = request.POST['username']
    password = request.POST['password']

    token = tellonym_utils.get_token(username, password)
    if isinstance(token, str):
        try:
            TellonymUser.create(username, token)
        except IntegrityError:
            hashed_username = hash_text(username)
            hashed_token = hash_text(token)
            user = TellonymUser.objects.get(hashed_username=hashed_username)
            user.hashed_token = hashed_token
            user.save()
        return JsonResponse({"Auth": token})
    return JsonResponse(token, status=401)


def get_tells(request):
    pass
    # Create your views here.
