from django.db import models
from apps.patients.models import Patient
from apps.staff.models import StaffProfile


class Room(models.Model):
    class Type(models.TextChoices):
        STANDARD = "standard", "Standard"
        DELUXE = "deluxe", "Deluxe"
        SUITE = "suite", "Suite"

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        OCCUPIED = "occupied", "Occupied"
        MAINTENANCE = "maintenance", "Maintenance"

    number = models.CharField(max_length=20, unique=True)
    room_type = models.CharField(max_length=20, choices=Type.choices, default=Type.STANDARD)
    floor = models.PositiveIntegerField(default=1)
    nightly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    class Meta:
        ordering = ["number"]


class RoomAvailability(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="availabilities")
    date = models.DateField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ("room", "date")


class Appointment(models.Model):
    class Status(models.TextChoices):
        BOOKED = "booked", "Booked"
        CHECKED_IN = "checked_in", "Checked In"
        CHECKED_OUT = "checked_out", "Checked Out"
        CANCELLED = "cancelled", "Cancelled"

    guest = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="bookings")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    assigned_staff = models.ForeignKey(
        StaffProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="managed_bookings"
    )
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.BOOKED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["check_in"]
