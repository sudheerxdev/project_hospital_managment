from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


def test_guest_signup_creates_guest_role_user(db):
    client = APIClient()
    payload = {
        "username": "guest_signup",
        "email": "guest@example.com",
        "first_name": "Guest",
        "last_name": "One",
        "phone": "1112223333",
        "password": "StrongPass123",
    }
    response = client.post("/api/auth/signup/", payload, format="json")

    assert response.status_code == 201
    assert "access" in response.data
    assert response.data["user"]["role"] == "guest"

    User = get_user_model()
    created = User.objects.get(username="guest_signup")
    assert created.role == User.Roles.GUEST
