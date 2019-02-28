import logging
from pymongo import MongoClient
from utils.config import conf


logger = logging.getLogger(__name__)


def exists(model, **kwargs):
    try:
        model.objects.get(**kwargs)
    except model.DoesNotExist:
        return False
    return True


def db_connection():
    return MongoClient(host=conf["database_uri"])


def geo_info_save(db, name, place_id, coordinate):
    collection = db[conf["database_name"]][conf["house_location_collection"]]
    geo_info = {
        "name": name,
        "place_id": place_id,
        "location":{
            "type": "Point",
            "coordinates":coordinate
        }
    }
    try:
        res = collection.insert_one(geo_info).inserted_id
        logger.info("House with name: {}, id: {} insert into Mongodb successfully".format(name, res))
    except Exception as e:
        logger.error(e)
        res = 0
    return res


if __name__ == "__main__":
    db = db_connection()
    res = geo_info_save(db, "test", "123qweasdzxc", [43.4791166,-80.5281053])
    print(res)