from django.conf import settings
from django.db import models
from apps.appointments.models import Appointment


class NotificationLog(models.Model):
    class Channel(models.TextChoices):
        EMAIL = "email", "Email"
        SMS = "sms", "SMS"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    recipient = models.CharField(max_length=150)
    channel = models.CharField(max_length=20, choices=Channel.choices)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    provider_response = models.TextField(blank=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="notifications", null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
