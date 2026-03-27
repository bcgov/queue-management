"""Log SMS payloads instead of sending them."""

from api.services.notification_logging import log_notification_payload

from . import SmsBaseService
from .payloads import build_gc_notify_sms_payload


class SmsLogNotify(SmsBaseService):
    """Implementation that logs GC Notify-shaped SMS payloads."""

    def send(self, sms_payload):
        """Log SMS reminders."""
        sms_requests = sms_payload if isinstance(sms_payload, list) else [sms_payload]

        for sms_request in sms_requests:
            if sms_request.get("user_telephone"):
                log_notification_payload("sms", build_gc_notify_sms_payload(sms_request))
