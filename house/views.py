import logging

from bson import ObjectId
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from db.dbutils import exists, db_connection, geo_info_save, geo_info_search
from utils import error_msg
from utils.login_utils import login_required
from utils.utils import image_to_str, str_to_datetime
from .models import House, Photo

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
        description = request.POST["description"]
    except KeyError as e:
        return JsonResponse({
            "success": 0,
            "msg": error_msg.MSG_400 + ': {}'.format(e)
        }, status=400)
    if exists(House, **{"name": name, "place_id": place_id, "address": address, "date_begin": date_begin,
                        "date_end": date_end}):
        logger.warning(
            "Failed to add new house, house with name: {}, place_id: {}, address:{} and date range {} to {} already exists.".format(
                name, place_id,
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
            number_of_beds=number_of_beds,
            description=description
        )
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
        res = geo_info_save(db, house.pk, place_id, coordinate)
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


@require_http_methods(["GET"])
@login_required
def search(request):
    try:
        if len(request.GET) == 0:
            no_arguments = True
        else:
            no_arguments = False
            longitude = request.GET["longitude"]
            latitude = request.GET["latitude"]
            date_begin = request.GET["date_begin"]
            date_end = request.GET["date_end"]
            num_of_beds = request.GET["number_of_beds"]
            max_distance = request.GET["max_distance"]
            if isinstance(num_of_beds, str):
                num_of_beds = int(num_of_beds)
            if isinstance(date_begin, str):
                date_begin = str_to_datetime(date_begin)
            if isinstance(date_end, str):
                date_end = str_to_datetime(date_end)
            if isinstance(max_distance, str):
                max_distance = int(max_distance)
    except KeyError as e:
        return JsonResponse({
            "success": 0,
            "msg": error_msg.MSG_400 + ': {}'.format(e)
        }, status=400)
    if no_arguments is False:
        coordinate = [float(longitude), float(latitude)]
        geo_search_res = geo_info_search(db, coordinate, max_distance)
        if not geo_search_res:
            logger.error(
                "Fail to search house with coordinate: {}. Something wrong with MongoDB.".format(str(coordinate)))
            return JsonResponse({
                "success": 0
            }, status=500)
        house_list = list()
        for each in geo_search_res:
            house = House.objects.get(pk=each["house_id"])
            if house.number_of_beds >= num_of_beds and house.date_begin <= date_begin and house.date_end >= date_end:
                house_info = house.dict_it()
                house_info["longitude"], house_info["latitude"] = each["location"]["coordinates"]
                house_list.append(house_info)
        return JsonResponse({
            "success": 1,
            "house_list": house_list
        })
    else:
        qs = House.objects.all()
        houses = qs[:10] if len(qs) >= 10 else qs
        return_house_list = [each.dict_it() for each in houses]
        return JsonResponse({
            "success": 1,
            "house_list": return_house_list
        })
