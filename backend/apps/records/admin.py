from django.contrib import admin
from .models import MedicalRecord, MedicalRecordVersion

admin.site.register(MedicalRecord)
admin.site.register(MedicalRecordVersion)
