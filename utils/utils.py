import base64
from datetime import date, datetime

from django.utils import timezone


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


def check_if_this_time_can_book(house, date_begin, date_end):
    from house.models import Booking
    query_set = Booking.objects.filter(**{"house": house})
    if not query_set:
        return True
    for each in query_set:
        # I don't want to combine all the if conditions together, it's not clear to see.
        if each.date_begin <= date_begin <= each.date_end or \
                each.date_end <= date_end <= each.date_end:
            return False
        if each.date_end > date_begin and each.end_date < date_end:
            return False
    return True


def get_time_zone_object():
    return datetime.now(tz=timezone.utc)
