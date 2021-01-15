from .models import TellonymUser, Tellonym
from .tellonym import tellonym_utils
from .utils import hash_text
from .authentication import get_user
from django.core import serializers
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_http_methods
import datetime
import json


@require_http_methods(["GET"])
def list_tellonyms(request):
    try:
        username = request.COOKIES['Username']
        token = request.COOKIES['Auth']
    except Exception:
        return HttpResponse(status=401)

    user = get_user(username, token)

    if isinstance(user, TellonymUser):
        tells = tellonym_utils.get_tells(token)
        user.add_tells(tells)
        json_tells = serializers.serialize('json', user.tellonym_set.filter(state='NEW'), fields=('text'))
        return HttpResponse(json_tells, content_type="application/json")
    raise Http404


@require_http_methods(["POST"])
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

        cookie_expire = datetime.datetime.now() + datetime.timedelta(days=369)
        response = JsonResponse({"Success": True}, status=200)
        response.set_cookie('Username', username, expires=cookie_expire, samesite='None', secure=True)
        response.set_cookie('Auth', token, expires=cookie_expire, samesite='None', secure=True)

        return response
    return JsonResponse(token, status=401)


@require_http_methods(["PATCH"])
def update_tellonym(request, tellonym_id):

    username = request.COOKIES.get('Username')
    token = request.COOKIES.get('Auth')

    user = get_user(username, token)

    if isinstance(user, TellonymUser):

        unicode_body = request.body.decode('utf-8')
        data = json.loads(unicode_body)

        tellonym = Tellonym.objects.get(pk=tellonym_id)
        tellonym.state = data['state']
        tellonym.save()

        return HttpResponse(status=204)

    return Http404
