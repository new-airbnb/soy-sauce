import logging

from bson import ObjectId
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from db.dbutils import exists, db_connection, geo_info_save
from utils import error_msg
from utils.login_utils import login_required
from .models import House, Photo
from utils.utils import image_to_str

logger = logging.getLogger(__name__)
db = db_connection()


@require_http_methods(["POST"])
@login_required
def create(request):
    try:
        name = request.POST["house_name"]
        place_id = request.POST["place_id"]
        address = request.POST["house_address"]
        city = request.POST["house_city"]
        province = request.POST["house_province"]
        postcode = request.POST["house_postcode"]
        longitude = request.POST["longitude"]
        latitude = request.POST["latitude"]
        coordinate = [float(longitude), float(latitude)]
        date_begin = request.POST["date_begin"]
        date_end = request.POST["date_end"]
        number_of_beds = request.POST["number_of_beds"]
    except KeyError as e:
        return JsonResponse({
            "success": 0,
            "msg": error_msg.MSG_400 + ': {}'.format(e)
        }, status=400)
    if exists(House, **{"name": name, "place_id": place_id, "address": address, "date_begin": date_begin, "date_end": date_end}):
        logger.warning(
            "Failed to add new house, house with name: {}, place_id: {}, address:{} and date range {} to {} already exists.".format(name, place_id,
                                                                                                      address, date_begin, date_end))
        return JsonResponse({
            "success": 0,
            "msg": error_msg.DUPLICATE_HOUSE
        })
    else:
        house = House(
                    name=name,
                    place_id=place_id,
                    address=address,
                    city=city,
                    province=province,
                    postcode=postcode,
                    date_begin=date_begin,
                    date_end=date_end,
                    number_of_beds=number_of_beds)
        if not house.date_is_valid():
            return JsonResponse({
                "success": 0,
                "msg": error_msg.WRONG_DATE_BEGIN_END
            }, status=400)
        try:
            house.save()
        except ValidationError as e:
            return JsonResponse({
                "success": 0,
                "msg": str(e)
            }, status=400)
        res = geo_info_save(db, name, place_id, coordinate)
        if isinstance(res, ObjectId):
            return JsonResponse({
                "success": 1,
                "info": {
                    "house_id": str(house.pk),
                    "geo_object_id": str(res)
                }
            })
        else:
            logger.error("Fail to save geo info of house: {}. Something wrong with MongoDB.".format(name))
            return JsonResponse({
                "success": 0
            }, status=500)


@require_http_methods(["POST"])
@login_required
def upload_photo(request):
    house_id = request.POST["house_id"]
    photo_file = request.FILES["photo"]
    try:
        house = House.objects.get(pk=int(house_id))
        _base64_str = image_to_str(photo_file)
        if _base64_str:
            photo = Photo(house=house, photo=_base64_str)
            photo.save()
            return JsonResponse({
                "success": 1,
                "info": {
                    "photo_id": str(photo.pk)
                }
            })
        else:
            return JsonResponse({
                "success": 0,
                "msg": error_msg.TOO_LARGE_IMAGE
            })
    except Exception as e:
        return JsonResponse({
            "success": 0,
            "msg": str(e)
        })
