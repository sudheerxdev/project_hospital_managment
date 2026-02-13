from django.db import models
from django.conf import settings
from apps.patients.models import Patient
from apps.common.security import FieldEncryptor

encryptor = FieldEncryptor()


class MedicalRecord(models.Model):
    class RecordType(models.TextChoices):
        ROOM_SERVICE = "room_service", "Room Service"
        HOUSEKEEPING = "housekeeping", "Housekeeping"
        MAINTENANCE = "maintenance", "Maintenance"

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="records")
    record_type = models.CharField(max_length=30, choices=RecordType.choices)
    title = models.CharField(max_length=200)
    payload = models.JSONField(default=dict)
    encrypted_notes = models.TextField(blank=True)
    current_version = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_notes(self, plain_text: str):
        self.encrypted_notes = encryptor.encrypt(plain_text)

    def get_notes(self):
        return encryptor.decrypt(self.encrypted_notes)


class MedicalRecordVersion(models.Model):
    record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name="versions")
    version_number = models.PositiveIntegerField()
    payload_snapshot = models.JSONField(default=dict)
    encrypted_notes_snapshot = models.TextField(blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("record", "version_number")
        ordering = ["-version_number"]
