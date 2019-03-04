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


def index_check(client):
    _collection = client[conf["database_name"]][conf["house_location_collection"]]
    if "location_2dsphere" not in _collection.index_information():
        _collection.create_index([("location", "2dsphere")])


def db_connection():
    client = MongoClient(host=conf["database_uri"])
    index_check(client)
    return client


def geo_info_save(db, house_id, place_id, coordinate):
    collection = db[conf["database_name"]][conf["house_location_collection"]]
    geo_info = {
        "house_id": house_id,
        "place_id": place_id,
        "location": {
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


def geo_info_search(db, coordinate, max_distance=20 * 1000):
    collection = db[conf["database_name"]][conf["house_location_collection"]]
    _GeoJSON = {
        "location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": coordinate
                },
                "$maxDistance": max_distance,
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
    res = geo_info_save(db, "test", "123qweasdzxc", [43.4791166, -80.5281053])
    print(res)
