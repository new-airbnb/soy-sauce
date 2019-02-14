import logging


logger = logging.getLogger(__name__)


def exists(model, **kwargs):
    try:
        model.objects.get(**kwargs)
    except model.DoesNotExist:
        return False
    return True