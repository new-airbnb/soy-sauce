from django.db import models

from utils.utils import get_timestamp


# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=128, db_index=True)
    password = models.CharField(max_length=64)
    type = models.CharField(
        max_length=16,
        choices=[
            ('admin', 'admin'),
            ('user', 'user')
        ],
        default='user')
    create_at = models.DateTimeField(default=get_timestamp)
