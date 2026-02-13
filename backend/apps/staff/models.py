from django.conf import settings
from django.db import models


class StaffProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile")
    specialization = models.CharField(max_length=120, blank=True)
    license_number = models.CharField(max_length=80, blank=True)
    shift_start = models.TimeField(null=True, blank=True)
    shift_end = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.role})"
