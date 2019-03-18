from django.db import models

from utils.utils import get_date_timestamp, get_time_zone_object


class House(models.Model):
    """House Model"""
    name = models.CharField(max_length=64)
    place_id = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=64)
    PROVINCES = [
        ("ON", "Ontario"),
        ("QC", "Quebec"),
        ("NS", "Nova Scotia"),
        ("NB", "New Brunswick"),
        ("MB", "Manitoba"),
        ("BC", "British Columbia"),
        ("PE", "Prince Edward Island"),
        ("SK", "Saskatchewan"),
        ("AB", "Alberta"),
        ("NL", "Newfoundland and Labrador")
    ]
    province = models.CharField(max_length=2, choices=PROVINCES, default="ON")
    postcode = models.CharField(max_length=6)
    date_begin = models.DateField(default=get_date_timestamp)
    date_end = models.DateField(default=get_date_timestamp)
    number_of_beds = models.PositiveIntegerField(default=1)
    create_at = models.DateTimeField(default=get_time_zone_object)
    description = models.CharField(max_length=200, default="no description")

    def date_is_valid(self):
        return self.date_end > self.date_begin

    def dict_it(self):
        return {
            "name": self.name,
            "place_id": self.place_id,
            "house_id": self.pk,
            "address": self.address,
            "city": self.city,
            "province": self.province,
            "postcode": self.postcode,
            "date_begin": self.date_begin,
            "date_end": self.date_end,
            "number_of_beds": self.number_of_beds,
            "description": self.description,
            "create_at": self.create_at
        }

    class Meta:
        ordering = ["-create_at"]


class Photo(models.Model):
    """Photo Model"""
    house = models.ForeignKey('house.House', on_delete=models.CASCADE)
    photo = models.CharField(max_length=10240000)
    upload_at = models.DateTimeField(default=get_time_zone_object)


class Booking(models.Model):
    """Booking Model"""
    house = models.ForeignKey('house.House', on_delete=models.CASCADE)
    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    date_begin = models.DateField(default=get_date_timestamp)
    date_end = models.DateField(default=get_date_timestamp)
    create_at = models.DateTimeField(default=get_time_zone_object)

    def date_is_valid(self):
        return self.date_end > self.date_begin
