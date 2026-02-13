from rest_framework import serializers
from .models import MedicalRecord, MedicalRecordVersion


class MedicalRecordVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecordVersion
        fields = "__all__"


class MedicalRecordSerializer(serializers.ModelSerializer):
    guest = serializers.IntegerField(source="patient", required=True)
    notes = serializers.CharField(write_only=True, required=False, allow_blank=True)
    decrypted_notes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MedicalRecord
        fields = [
            "id",
            "guest",
            "record_type",
            "title",
            "payload",
            "notes",
            "decrypted_notes",
            "current_version",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["current_version", "created_by", "created_at", "updated_at"]

    def get_decrypted_notes(self, obj):
        return obj.get_notes()

    def create(self, validated_data):
        notes = validated_data.pop("notes", "")
        record = MedicalRecord(**validated_data)
        record.set_notes(notes)
        record.save()
        MedicalRecordVersion.objects.create(
            record=record,
            version_number=record.current_version,
            payload_snapshot=record.payload,
            encrypted_notes_snapshot=record.encrypted_notes,
            updated_by=record.created_by,
        )
        return record

    def update(self, instance, validated_data):
        notes = validated_data.pop("notes", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if notes is not None:
            instance.set_notes(notes)
        instance.current_version += 1
        instance.save()
        MedicalRecordVersion.objects.create(
            record=instance,
            version_number=instance.current_version,
            payload_snapshot=instance.payload,
            encrypted_notes_snapshot=instance.encrypted_notes,
            updated_by=self.context["request"].user,
        )
        return instance
