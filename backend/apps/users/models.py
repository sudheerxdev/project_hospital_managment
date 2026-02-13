from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        MANAGER = "manager", "Manager"
        FRONT_DESK = "front_desk", "Front Desk"
        HOUSEKEEPING = "housekeeping", "Housekeeping"
        ACCOUNTANT = "accountant", "Accountant"
        GUEST = "guest", "Guest"

    role = models.CharField(max_length=20, choices=Roles.choices)
    phone = models.CharField(max_length=20, blank=True)
