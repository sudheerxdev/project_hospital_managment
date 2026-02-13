from django.conf import settings
from django.db import models


class Patient(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="patient_profile"
    )
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=5, blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="history")
    condition = models.CharField(max_length=120)
    details = models.TextField(blank=True)
    diagnosed_on = models.DateField(null=True, blank=True)
    is_chronic = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
