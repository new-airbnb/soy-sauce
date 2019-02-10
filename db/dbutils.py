import logging
from pymodm.connection import connect


logger = logging.getLogger(__name__)


def connect_db(uri):
    try:
        connect(uri)
        logger.info("[DB] uri:{}".format(uri))
    except Exception as e:
        logger.exception("Fail to connect database. Exception: {}".format(e))
        raise e


def exists(model, query):
    res = model.objects.raw(query)
    return res.count() != 0