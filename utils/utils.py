from datetime import date, datetime
import base64


def get_date_timestamp(t=None):
    # used for django model default value when migrate
    # migration doesn't support lambda
    return get_timestamp(t, with_time=False)


def get_timestamp(t=None, with_time=True):
    if t:
        dt = t
    elif with_time:
        dt = datetime.utcnow()
    else:
        dt = date.today()
    s = dt.isoformat()
    if with_time:
        return s + 'Z'
    else:
        return s


def str_to_datetime(t):
    d = datetime.strptime(t, "%Y-%m-%d")
    return date(d.year, d.month, d.day)


def str_to_boolean(string):
    if string.upper() == "TRUE":
        return True
    else:
        return False


MAX_IMAGE_SIZE = 10240000


def image_to_str(image):
    with image.open("rb") as f:
        string = base64.b64encode(f.read())
        if len(string) > MAX_IMAGE_SIZE:
            return None
        return string


def get_current_user_id(request):
    current_user = request.user
    return current_user.pk
