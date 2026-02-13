from datetime import timedelta, date
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.patients.models import Patient
from apps.appointments.models import Appointment, Room


def test_e2e_booking_and_invoicing(db):
    User = get_user_model()
    manager = User.objects.create_user(username="manager2", password="adminpass123", role=User.Roles.MANAGER)
    guest = Patient.objects.create(first_name="Eve", last_name="R", date_of_birth=date(1994, 2, 12), gender="female")
    room = Room.objects.create(number="302", room_type=Room.Type.SUITE, floor=3, nightly_rate=220)

    booking = Appointment.objects.create(
        guest=guest,
        room=room,
        check_in=timezone.now() + timedelta(days=2),
        check_out=timezone.now() + timedelta(days=4),
        notes="Late arrival",
    )

    client = APIClient()
    client.force_authenticate(user=manager)
    response = client.post("/api/invoices/generate/", {"booking": booking.id}, format="json")

    assert response.status_code == 200
    assert response.data["booking"] == booking.id
    assert response.data["status"] == "issued"
