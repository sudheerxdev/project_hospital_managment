from django.contrib.auth import get_user_model


def test_create_user_model(db):
    User = get_user_model()
    user = User.objects.create_user(username="manager1", password="xpass123", role=User.Roles.MANAGER)
    assert user.role == User.Roles.MANAGER
    assert user.check_password("xpass123")
