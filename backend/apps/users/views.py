from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.permissions import RolePermission
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [RolePermission]
    allowed_roles = [User.Roles.ADMIN, User.Roles.MANAGER]


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def signup(self, request):
        payload = request.data.copy()
        payload["role"] = User.Roles.GUEST
        serializer = UserSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        warning = None

        try:
            user = serializer.save()
        except IntegrityError as exc:
            # Compatibility fallback for old databases that still enforce legacy role constraints.
            if "role" in str(exc).lower():
                legacy_payload = request.data.copy()
                legacy_payload["role"] = "patient"
                legacy_serializer = UserSerializer(data=legacy_payload)
                legacy_serializer.is_valid(raise_exception=True)
                user = legacy_serializer.save()
                warning = "Legacy role constraint detected. Run migrations to enable guest role."
            else:
                raise

        refresh = RefreshToken.for_user(user)
        response_payload = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        }
        if warning:
            response_payload["warning"] = warning
        return Response(response_payload, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data,
            }
        )

    @action(detail=False, methods=["post"])
    def logout(self, request):
        token = request.data.get("refresh")
        if token:
            try:
                RefreshToken(token).blacklist()
            except Exception:
                pass
        return Response({"detail": "Logged out"})
