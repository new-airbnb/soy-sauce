from datetime import date, datetime


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


def house_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/house_<name>/<filename>
    return 'house_{0}/{1}'.format(instance.house.pk, filename)
