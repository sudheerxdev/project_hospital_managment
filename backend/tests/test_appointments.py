from datetime import date, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.patients.models import Patient
from apps.staff.models import StaffProfile
from apps.appointments.models import Appointment, Room


def test_booking_flow(db):
    User = get_user_model()
    staff_user = User.objects.create_user(username="front1", password="xpass123", role=User.Roles.FRONT_DESK)
    staff = StaffProfile.objects.create(user=staff_user, specialization="Front Office")
    guest = Patient.objects.create(first_name="Alice", last_name="P", date_of_birth=date(1999, 6, 6), gender="female")
    room = Room.objects.create(number="101", room_type=Room.Type.DELUXE, floor=1, nightly_rate=140)
    booking = Appointment.objects.create(
        guest=guest,
        room=room,
        assigned_staff=staff,
        check_in=timezone.now() + timedelta(days=1),
        check_out=timezone.now() + timedelta(days=2),
    )
    assert booking.status == Appointment.Status.BOOKED
