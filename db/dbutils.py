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


def geo_info_save(db, house_id, place_id, coordinate):
    collection = db[conf["database_name"]][conf["house_location_collection"]]
    collection.ensure_index([("location", "2dsphere")])
    geo_info = {
        "house_id": house_id,
        "place_id": place_id,
        "location":{
            "type": "Point",
            "coordinates": coordinate
        }
    }
    try:
        res = collection.insert_one(geo_info).inserted_id
        logger.info("House with id: {}, id: {} insert into Mongodb successfully".format(house_id, res))
    except Exception as e:
        logger.error(e)
        res = 0
    return res


def geo_info_search(db, coordinate):
    collection = db[conf["database_name"]][conf["house_location_collection"]]
    _GeoJSON = {
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": coordinate
                },
                "$maxDistance": 20*1000,
                "$minDistance": 0
            }
        }
    }
    try:
        cursor = collection.find(_GeoJSON)
    except Exception as e:
        logger.error(e)
        cursor = None
    return cursor


HOUSE_COLLECTION = "house_house"


def collection_find(db, **kwargs):
    collection = db[conf["database_name"][HOUSE_COLLECTION]]
    try:
        cursor = collection.find(kwargs)
    except Exception as e:
        logger.error(e)
        cursor = None
    return cursor


if __name__ == "__main__":
    db = db_connection()
    res = geo_info_save(db, "test", "123qweasdzxc", [43.4791166,-80.5281053])
    print(res)