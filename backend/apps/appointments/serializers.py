from rest_framework import serializers
from .models import Appointment, RoomAvailability, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class RoomAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAvailability
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, attrs):
        start = attrs.get("check_in")
        end = attrs.get("check_out")
        if start and end and end <= start:
            raise serializers.ValidationError("Check-out must be after check-in.")
        return attrs
