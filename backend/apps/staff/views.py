from rest_framework import viewsets
from django.contrib.auth import get_user_model

from apps.common.permissions import RolePermission
from .models import StaffProfile
from .serializers import StaffProfileSerializer

User = get_user_model()


class StaffProfileViewSet(viewsets.ModelViewSet):
    queryset = StaffProfile.objects.select_related("user").all().order_by("id")
    serializer_class = StaffProfileSerializer
    permission_classes = [RolePermission]
    allowed_roles = [User.Roles.ADMIN, User.Roles.MANAGER]
