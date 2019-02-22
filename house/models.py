from django.db import models

from utils.utils import get_timestamp, house_directory_path


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
    create_at = models.DateTimeField(default=get_timestamp)


class Photo(models.Model):
    """Photo Model"""
    house = models.ForeignKey('house.House', on_delete=models.CASCADE)
    photo = models.FileField(upload_to=house_directory_path)
    upload_at = models.DateTimeField(default=get_timestamp)
