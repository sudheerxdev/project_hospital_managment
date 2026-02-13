from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import RolePermission
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer, MedicalRecordVersionSerializer

User = get_user_model()


class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.select_related("patient", "created_by").all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [RolePermission]
    allowed_roles = [User.Roles.ADMIN, User.Roles.MANAGER, User.Roles.FRONT_DESK, User.Roles.HOUSEKEEPING]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["get"])
    def versions(self, request, pk=None):
        record = self.get_object()
        versions = record.versions.all()
        return Response(MedicalRecordVersionSerializer(versions, many=True).data)


# Backward compatible alias
MedicalRecordViewSet = ServiceRequestViewSet
