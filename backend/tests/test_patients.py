from datetime import date

from apps.patients.models import Patient


def test_patient_creation(db):
    patient = Patient.objects.create(
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
        gender="male",
    )
    assert patient.id is not None
    assert patient.first_name == "John"
