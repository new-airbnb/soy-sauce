import logging

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import User
from db.dbutils import exists
from utils import error_msg
from utils.login_utils import login_user, login_required
from utils.utils import str_to_boolean


logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
def register(request):
    email, password = request.POST["email"], request.POST["password"]
    if exists(User, **{"email": email}):
        logger.warning("Failed to add new user: email {} already exists".format(email))
        return JsonResponse({
            "success": 0,
            "msg": error_msg.DUPLICATE_EMAIL
        }, status=409)

    try:
        user = User(email=email, password=password, type='user')
        user.save()
    except ValidationError as e:
        return JsonResponse({
            'success': 0,
            'msg': error_msg.ILLEGAL_ARGUMENT
        }, status=400)

    return JsonResponse({
        "success": 1,
        "user": {
            "email": user.email
        }
    })


@require_http_methods(["POST"])
def login(request):
    try:
        email = request.POST["email"]
        password = request.POST["password"]
        remember_me = request.POST["remember_me"]
    except KeyError:
        return JsonResponse({
            'success': 0,
            'msg': error_msg.ILLEGAL_ARGUMENT
        }, status=400)

    if not isinstance(remember_me, bool):
        remember_me = str_to_boolean(remember_me)
    try:
        user = User.objects.get(**{"email": email, "password": password})
    except:
        return JsonResponse({
            "success": 0,
            "msg": error_msg.WRONG_PASSWORD_OR_EMAIL_ADDRESS
        }, status=401)
    login_user(request.session, user, remember_me)
    return JsonResponse({
        "success": 1
    })


@require_http_methods(["GET"])
@login_required
def check_login(request):
    return JsonResponse({
        "success": 1,
        "msg": "user: {} sign in successfully.".format(request.session['user']['email'])
    })


@require_http_methods(["GET", "POST"])
@login_required
def logout(request):
    del request.session['user']
    return JsonResponse({
        "success": 1
    })
