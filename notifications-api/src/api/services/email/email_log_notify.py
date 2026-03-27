"""Log email payloads instead of sending them."""

from api.services.notification_logging import log_notification_payload

from . import EmailBaseService
from .payloads import build_gc_notify_email_payload


class EmailLogNotify(EmailBaseService):
    """Implementation that logs GC Notify-shaped email payloads."""

    def send(self, email_payload):
        """Log an email payload."""
        log_notification_payload("email", build_gc_notify_email_payload(email_payload))
