from .models import TellonymUser, Tellonym
from .tellonym import tellonym_utils
from .utils import hash_text, error_dict
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
        username = request.headers['Username']
        token = request.headers['Auth']
    except Exception:
        return JsonResponse(error_dict('Nie jesteś zalogowany'), status=401)

    user = get_user(username, token)

    if isinstance(user, TellonymUser):
        tells = tellonym_utils.get_tells(token)
        user.add_tells(tells)
        json_tells = serializers.serialize('json', user.tellonym_set.filter(state='NEW').order_by('-pk'), fields=('text'))
        return HttpResponse(json_tells, content_type="application/json")
    raise Http404


@require_http_methods(["POST"])
def login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            raise KeyError
    except KeyError:
        return JsonResponse(error_dict('Wypełnij wszystkie pola formularza'))

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

        response = JsonResponse({"Success": True,
                                 'Username': username,
                                 'Auth': token
                                 }, status=200)
        cookie_expire = datetime.datetime.now() + datetime.timedelta(days=369)
        response.set_cookie('Username', username, expires=cookie_expire, samesite='None', secure=True)
        response.set_cookie('Auth', token, expires=cookie_expire, samesite='None', secure=True)

        return response
    return JsonResponse(token, status=200)


@require_http_methods(["PATCH"])
def update_tellonym(request, tellonym_id):
    try:
        username = request.headers['Username']
        token = request.headers['Auth']
    except Exception:
        return JsonResponse(error_dict('Nie jesteś zalogowany'), status=401)

    user = get_user(username, token)

    if isinstance(user, TellonymUser):

        unicode_body = request.body.decode('utf-8')
        data = json.loads(unicode_body)

        tellonym = Tellonym.objects.get(pk=tellonym_id)
        tellonym.state = data['state']
        if "text" in data:
            tellonym.text = data['text']
        tellonym.save()

        return HttpResponse(status=204)

    return JsonResponse(error_dict("Nie jesteś zalogowany"), status=401)
