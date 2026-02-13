from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from apps.common.permissions import RolePermission
from .models import Patient, MedicalHistory
from .serializers import PatientSerializer, MedicalHistorySerializer

User = get_user_model()


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [RolePermission]
    allowed_roles = [User.Roles.ADMIN, User.Roles.MANAGER, User.Roles.FRONT_DESK]

    def get_queryset(self):
        queryset = super().get_queryset()
        term = self.request.query_params.get("search")
        if term:
            queryset = queryset.filter(
                Q(first_name__icontains=term)
                | Q(last_name__icontains=term)
                | Q(email__icontains=term)
                | Q(phone__icontains=term)
            )
        return queryset

    @action(detail=True, methods=["get"])
    def full_history(self, request, pk=None):
        guest = self.get_object()
        payload = {
            "guest": PatientSerializer(guest).data,
            "stay_history": MedicalHistorySerializer(guest.history.all(), many=True).data,
        }
        return Response(payload)


class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.select_related("patient").all()
    serializer_class = MedicalHistorySerializer
    permission_classes = [RolePermission]
    allowed_roles = [User.Roles.ADMIN, User.Roles.MANAGER, User.Roles.FRONT_DESK]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
