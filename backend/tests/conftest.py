import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username="admin", password="adminpass123", role=User.Roles.ADMIN)


@pytest.fixture
def api_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client
