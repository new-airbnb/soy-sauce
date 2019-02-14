from functools import wraps

from django.http import JsonResponse

from db.dbutils import exists
from user.models import User
from utils import error_msg


def login_user(session, user, remember):
    session['user'] = {
        'email': user.email,
        'type': user.type
    }
    expiry = 3600 * 24
    if remember:
        expiry *= 30
    session.set_expiry(expiry)


def login_required(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        s = request.session
        if 'user' not in s \
            or 'email' not in s['user'] \
            or not exists(User, email=s['user']['email']):
            return JsonResponse({
                "success": 0,
                'msg': error_msg.MSG_403
            }, status=403)
        return f(request, *args, **kwargs)
    return wrapper
