from urllib import request as urllib_request
from urllib.error import URLError, HTTPError
import json

from django.conf import settings
from django.core.mail import send_mail


class NotificationDeliveryError(Exception):
    pass


def send_email_notification(recipient: str, message: str):
    send_mail(
        subject="StayFlow Notification",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient],
        fail_silently=False,
    )


def send_sms_notification(recipient: str, message: str):
    if not settings.SMS_WEBHOOK_URL:
        raise NotificationDeliveryError("SMS webhook is not configured")

    payload = json.dumps({"to": recipient, "message": message}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if settings.SMS_WEBHOOK_TOKEN:
        headers["Authorization"] = f"Bearer {settings.SMS_WEBHOOK_TOKEN}"

    req = urllib_request.Request(settings.SMS_WEBHOOK_URL, data=payload, headers=headers, method="POST")
    try:
        with urllib_request.urlopen(req, timeout=8) as resp:
            if resp.status >= 300:
                raise NotificationDeliveryError(f"SMS provider returned status {resp.status}")
    except (HTTPError, URLError) as exc:
        raise NotificationDeliveryError(str(exc)) from exc


def dispatch_notification(channel: str, recipient: str, message: str):
    if channel == "email":
        send_email_notification(recipient, message)
        return
    if channel == "sms":
        send_sms_notification(recipient, message)
        return
    raise NotificationDeliveryError(f"Unsupported channel: {channel}")
