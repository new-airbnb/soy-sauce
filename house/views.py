import logging

from bson import ObjectId
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from db.dbutils import exists, db_connection, geo_info_save
from utils import error_msg
from .models import House, Photo
from utils.login_utils import login_required

logger = logging.getLogger(__name__)
db = db_connection()


@require_http_methods(["POST"])
@login_required
def create(request):
    name = request.POST["house_name"]
    place_id = request.POST["place_id"]
    address = request.POST["house_address"]
    city = request.POST["house_city"]
    province = request.POST["house_province"]
    postcode = request.POST["house_postcode"]
    coordinate = request.POST["house_coordinate"]
    if isinstance(coordinate, str):
        coordinate = [float(i) for i in coordinate.lstrip("[").rstrip("]").split(",")]
    if exists(House, **{"name": name, "place_id": place_id, "address": address}):
        logger.warning(
            "Failed to add new house, house with name: {}, id: {}, address:{} already exists.".format(name, id,
                                                                                              address))
        return JsonResponse({
            "success": 0,
            "msg": error_msg.DUPLICATE_HOUSE
        })
    else:
        try:
            house = House(name=name, place_id=place_id, address=address, city=city, province=province, postcode=postcode)
            house.save()
        except ValidationError as e:
            return JsonResponse({
                "success": 0,
                "msg": str(e)
            })
        res = geo_info_save(db, name, place_id, coordinate)
        if isinstance(res, ObjectId):
            return JsonResponse({
                "success": 1,
                "info":{
                    "house_id": str(house.pk),
                    "geo_object_id": str(res)
                }
            })
        else:
            return JsonResponse({
                "success": 0
            }), 500


@require_http_methods(["POST"])
@login_required
def upload_photo(request):
    house_id = request.POST["house_id"]
    photo_file = request.FILES["photo"]
    try:
        house = House.objects.get(pk=int(house_id))
        photo = Photo(house=house, photo=photo_file)
        photo.save()
        return JsonResponse({
            "success": 1,
            "info":{
                "photo_id": str(photo.pk)
            }
        })
    except Exception as e:
        return JsonResponse({
            "success": 0,
            "msg": str(e)
        })
