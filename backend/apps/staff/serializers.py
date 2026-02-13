from rest_framework import serializers
from .models import StaffProfile


class StaffProfileSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = StaffProfile
        fields = [
            "id",
            "user",
            "user_full_name",
            "specialization",
            "license_number",
            "shift_start",
            "shift_end",
        ]
