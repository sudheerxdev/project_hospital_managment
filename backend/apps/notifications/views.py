from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import RolePermission
from .models import NotificationLog
from .serializers import NotificationLogSerializer
from .services import dispatch_notification, NotificationDeliveryError

User = get_user_model()


class NotificationLogViewSet(viewsets.ModelViewSet):
    queryset = NotificationLog.objects.select_related("appointment").all().order_by("-sent_at")
    serializer_class = NotificationLogSerializer
    permission_classes = [RolePermission]
    allowed_roles = [User.Roles.ADMIN, User.Roles.MANAGER, User.Roles.FRONT_DESK]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=["post"])
    def send_reminder(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        log = serializer.save(created_by=request.user, status=NotificationLog.Status.PENDING)
        try:
            dispatch_notification(log.channel, log.recipient, log.message)
            log.status = NotificationLog.Status.SENT
            log.provider_response = "Delivered"
            log.save(update_fields=["status", "provider_response"])
            return Response({"detail": "Reminder sent", "id": log.id})
        except NotificationDeliveryError as exc:
            log.status = NotificationLog.Status.FAILED
            log.provider_response = str(exc)
            log.save(update_fields=["status", "provider_response"])
            return Response(
                {"detail": f"Notification failed: {exc}", "id": log.id},
                status=status.HTTP_502_BAD_GATEWAY,
            )
