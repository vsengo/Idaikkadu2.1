import uuid
import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField('First Name of User', blank=True, max_length=20)
    last_name = models.CharField('Last Name of User', blank=True, max_length=20)


class Meta:
    permissions = (("view_add_delete", "To provide update edit facility"),
                   ("view_add", "To provide add facility"),
                   ("view_only", "To provide update view facility"))
