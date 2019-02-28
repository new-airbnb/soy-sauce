from django.db import models

from utils.utils import get_date_timestamp, get_timestamp


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
    create_at = models.DateTimeField(default=get_date_timestamp)

    def date_is_valid(self):
        return self.date_end > self.date_begin


class Photo(models.Model):
    """Photo Model"""
    house = models.ForeignKey('house.House', on_delete=models.CASCADE)
    photo = models.CharField(max_length=10240000)
    upload_at = models.DateTimeField(default=get_timestamp)
