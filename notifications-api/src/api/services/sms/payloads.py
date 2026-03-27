"""Payload builders for SMS providers."""

from flask import current_app


def construct_sms_text(sms_request: dict) -> str:
    """Construct the SMS text using the current templates."""
    message_type: str = sms_request.get("type", "REMINDER")
    template = ""
    app_url = current_app.config.get("APPOINTMENT_APP_URL", "")
    if message_type == "REMINDER":
        template = current_app.config.get("SMS_REMINDER_TEMPLATE", "")
    elif message_type == "CHECKIN_CONFIRMATION":
        template = current_app.config.get("SMS_CHECKIN_CONFIRMATION_TEMPLATE", "")
    elif message_type == "CUSTOM":
        return sms_request.get("message", "")

    return template.format(app_url=app_url, **sms_request) if template else ""


def build_gc_notify_sms_payload(sms_request: dict) -> dict:
    """Build the GC Notify SMS payload shape."""
    return {
        "phone_number": sms_request.get("user_telephone"),
        "template_id": current_app.config["GC_NOTIFY_SMS_TEMPLATE_ID"],
        "personalisation": {
            "sms_text": construct_sms_text(sms_request),
        },
    }
