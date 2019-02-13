from datetime import datetime


def get_timestamp(t=None):
    dt = t if t else datetime.utcnow()
    return dt.isoformat() + 'Z'


def str_to_boolean(string):
    if string == "True":
        return True
    else:
        return False
