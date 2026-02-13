from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views import UserViewSet, AuthViewSet
from apps.staff.views import StaffProfileViewSet
from apps.patients.views import PatientViewSet, MedicalHistoryViewSet
from apps.appointments.views import BookingViewSet, RoomAvailabilityViewSet, RoomViewSet
from apps.records.views import ServiceRequestViewSet
from apps.billing.views import BillViewSet
from apps.dashboard.views import DashboardView
from apps.notifications.views import NotificationLogViewSet
from apps.common.views import health_view

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"auth", AuthViewSet, basename="auth")
router.register(r"staff", StaffProfileViewSet, basename="staff")
router.register(r"guests", PatientViewSet, basename="guests")
router.register(r"guest-history", MedicalHistoryViewSet, basename="guest-history")
router.register(r"rooms", RoomViewSet, basename="rooms")
router.register(r"bookings", BookingViewSet, basename="bookings")
router.register(r"room-availability", RoomAvailabilityViewSet, basename="room-availability")
router.register(r"services", ServiceRequestViewSet, basename="services")
router.register(r"invoices", BillViewSet, basename="invoices")
router.register(r"notifications", NotificationLogViewSet, basename="notifications")

router.register(r"patients", PatientViewSet, basename="patients")
router.register(r"appointments", BookingViewSet, basename="appointments")
router.register(r"records", ServiceRequestViewSet, basename="records")
router.register(r"bills", BillViewSet, basename="bills")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/dashboard/", DashboardView.as_view(), name="dashboard"),
    path("api/health/", health_view, name="health"),
]
