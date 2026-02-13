from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from apps.appointments.models import Appointment, Room
from apps.patients.models import Patient
from apps.staff.models import StaffProfile
from apps.billing.models import Bill
from apps.common.permissions import RolePermission

User = get_user_model()


class DashboardView(APIView):
    permission_classes = [RolePermission]
    allowed_roles = [
        User.Roles.ADMIN,
        User.Roles.MANAGER,
        User.Roles.FRONT_DESK,
        User.Roles.ACCOUNTANT,
        User.Roles.HOUSEKEEPING,
        User.Roles.GUEST,
    ]

    def get(self, request):
        now = timezone.now()
        upcoming_bookings = Appointment.objects.filter(
            check_out__gte=now,
            status__in=[Appointment.Status.BOOKED, Appointment.Status.CHECKED_IN],
        )[:10].values("id", "guest_id", "room_id", "check_in", "check_out", "status")

        payload = {
            "total_guests": Patient.objects.count(),
            "total_staff": StaffProfile.objects.count(),
            "total_rooms": Room.objects.count(),
            "occupied_rooms": Room.objects.filter(status=Room.Status.OCCUPIED).count(),
            "today_check_ins": Appointment.objects.filter(check_in__date=now.date()).count(),
            "upcoming_bookings": list(upcoming_bookings),
            "pending_invoices": Bill.objects.filter(status=Bill.Status.ISSUED).count(),
            # Backward compatibility keys
            "total_patients": Patient.objects.count(),
            "today_appointments": Appointment.objects.filter(check_in__date=now.date()).count(),
            "upcoming_appointments": list(upcoming_bookings),
            "pending_bills": Bill.objects.filter(status=Bill.Status.ISSUED).count(),
        }
        return Response(payload)
