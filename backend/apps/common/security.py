from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
import base64
import hashlib


class FieldEncryptor:
    """Small Fernet wrapper for field-level encryption."""

    def __init__(self):
        key = settings.FIELD_ENCRYPTION_KEY or settings.SECRET_KEY
        digest = hashlib.sha256(key.encode("utf-8")).digest()
        self.fernet = Fernet(base64.urlsafe_b64encode(digest))

    def encrypt(self, value: str) -> str:
        if not value:
            return ""
        return self.fernet.encrypt(value.encode("utf-8")).decode("utf-8")

    def decrypt(self, value: str) -> str:
        if not value:
            return ""
        try:
            return self.fernet.decrypt(value.encode("utf-8")).decode("utf-8")
        except InvalidToken:
            return ""
