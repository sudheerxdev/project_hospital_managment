from datetime import date
from django.contrib.auth import get_user_model

from apps.patients.models import Patient
from apps.records.models import MedicalRecord


def test_service_request_versioning(db):
    User = get_user_model()
    creator = User.objects.create_user(username="ops1", password="xpass123", role=User.Roles.MANAGER)
    guest = Patient.objects.create(first_name="Bob", last_name="M", date_of_birth=date(1988, 3, 1), gender="male")
    request_record = MedicalRecord.objects.create(
        patient=guest,
        record_type=MedicalRecord.RecordType.ROOM_SERVICE,
        title="Extra towels",
        payload={"priority": "normal"},
        created_by=creator,
    )
    request_record.set_notes("Deliver before 8 PM")
    request_record.save()
    assert request_record.get_notes() == "Deliver before 8 PM"
