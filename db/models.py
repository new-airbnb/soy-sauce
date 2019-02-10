import pymongo
from pymodm import MongoModel, fields
from utils.utils import get_timestamp


class ModelWithCreateAt(MongoModel):
    """Base class"""
    create_at = fields.DateTimeField(required=True, default=get_timestamp)


class User(ModelWithCreateAt):
    email = fields.EmailField(required=True, blank=False)
    password = fields.CharField(required=True, blank=False)
    type = fields.CharField(required=True, blank=False, choices=['admin', 'user'], default='user')

    class Meta:
        indexes = [
            pymongo.IndexModel([('email', pymongo.ASCENDING)]),
        ]
