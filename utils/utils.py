from datetime import date, datetime
import base64


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


def str_to_boolean(string):
    if string == "True":
        return True
    else:
        return False


def image_to_str(image):
    with image.open("rb") as f:
        string = base64.b64encode(f.read())
        if len(string) > 10240000:
            return None
        return string
