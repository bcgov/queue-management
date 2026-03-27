"""Payload builders for email providers."""

from flask import current_app


def build_gc_notify_email_payload(email_payload: dict) -> dict:
    """Build the GC Notify email payload shape."""
    return {
        "email_address": ",".join(email_payload.get("to", [])),
        "template_id": current_app.config["GC_NOTIFY_EMAIL_TEMPLATE_ID"],
        "personalisation": {
            "email_subject": email_payload.get("subject"),
            "email_text": email_payload.get("body"),
        },
    }
