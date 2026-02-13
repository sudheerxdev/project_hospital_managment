from django.contrib import admin
from .models import Appointment, RoomAvailability, Room

admin.site.register(Room)
admin.site.register(Appointment)
admin.site.register(RoomAvailability)
