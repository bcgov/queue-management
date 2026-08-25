"""Helpers for logging notification payloads."""

import json
import logging
from typing import Any


LOGGER = logging.getLogger("api.services.notifications")


def log_notification_payload(channel: str, payload: dict[str, Any]) -> None:
    """Log a notification payload in a readable, stable format."""
    LOGGER.info(
        "%s notification payload:\n%s",
        channel.upper(),
        json.dumps(payload, indent=2, sort_keys=True),
    )
