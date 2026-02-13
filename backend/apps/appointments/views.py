from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import RolePermission
from .models import Appointment, RoomAvailability, Room
from .serializers import AppointmentSerializer, RoomAvailabilitySerializer, RoomSerializer

User = get_user_model()


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [RolePermission]
    allowed_roles = [User.Roles.ADMIN, User.Roles.MANAGER, User.Roles.FRONT_DESK]


class RoomAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = RoomAvailability.objects.select_related("room").all()
    serializer_class = RoomAvailabilitySerializer
    permission_classes = [RolePermission]
    allowed_roles = [User.Roles.ADMIN, User.Roles.MANAGER, User.Roles.FRONT_DESK]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related("guest", "room", "assigned_staff", "assigned_staff__user").all()
    serializer_class = AppointmentSerializer
    permission_classes = [RolePermission]
    allowed_roles = [User.Roles.ADMIN, User.Roles.MANAGER, User.Roles.FRONT_DESK]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_value = self.request.query_params.get("status")
        room_id = self.request.query_params.get("room")
        if status_value:
            queryset = queryset.filter(status=status_value)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        upcoming_only = self.request.query_params.get("upcoming")
        if upcoming_only == "true":
            queryset = queryset.filter(check_out__gte=timezone.now(), status__in=[Appointment.Status.BOOKED, Appointment.Status.CHECKED_IN])
        term = self.request.query_params.get("search")
        if term:
            queryset = queryset.filter(
                Q(guest__first_name__icontains=term)
                | Q(guest__last_name__icontains=term)
                | Q(notes__icontains=term)
                | Q(room__number__icontains=term)
            )
        return queryset

    @action(detail=True, methods=["post"])
    def reschedule(self, request, pk=None):
        booking = self.get_object()
        serializer = self.get_serializer(booking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(status=Appointment.Status.BOOKED)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        booking.status = Appointment.Status.CANCELLED
        booking.save(update_fields=["status"])
        return Response({"id": booking.id, "status": booking.status})


# Backward compatible aliases
AppointmentViewSet = BookingViewSet
DoctorAvailabilityViewSet = RoomAvailabilityViewSet
