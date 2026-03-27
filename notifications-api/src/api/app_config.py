# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Application configuration."""

import os
import sys

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

CONFIGURATION = {
    "production": "config.ProdConfig",
    "prod": "config.ProdConfig",
    "staging": "config.ProdConfig",
    "testing": "config.TestConfig",
    "test": "config.TestConfig",
    "development": "config.DevConfig",
    "dev": "config.DevConfig",
    "default": "config.ProdConfig",
}


def normalize_config_name(config_name: str | None = None) -> str:
    """Return the normalized configuration name."""
    requested = (
        config_name
        or os.getenv("FLASK_CONFIGURATION")
        or os.getenv("FLASK_ENV")
        or "default"
    )
    normalized = requested.lower()
    if normalized not in CONFIGURATION:
        raise KeyError(f"Unknown configuration '{requested}'")
    return normalized


def get_named_config(config_name: str | None = None):
    """Return the configuration object based on the name."""
    normalized = normalize_config_name(config_name)
    if normalized in {"production", "prod", "staging", "default"}:
        return ProdConfig()
    if normalized in {"testing", "test"}:
        return TestConfig()
    return DevConfig()


class _Config:  # pylint: disable=too-few-public-methods
    """Base configuration."""

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    TESTING = False
    DEBUG = False

    SECRET_KEY = os.getenv("SECRET_KEY")

    JWT_OIDC_WELL_KNOWN_CONFIG = os.getenv("JWT_OIDC_WELL_KNOWN_CONFIG")
    JWT_OIDC_ALGORITHMS = os.getenv("JWT_OIDC_ALGORITHMS", "RS256")
    JWT_OIDC_AUDIENCE = os.getenv("JWT_OIDC_AUDIENCE")
    JWT_OIDC_CLIENT_SECRET = os.getenv("JWT_OIDC_CLIENT_SECRET", "")
    JWT_OIDC_CACHING_ENABLED = os.getenv("JWT_OIDC_CACHING_ENABLED", "true").lower() == "true"
    JWT_OIDC_JWKS_CACHE_TIMEOUT = int(os.getenv("JWT_OIDC_JWKS_CACHE_TIMEOUT", "300"))

    SMS_PROVIDER = os.getenv("SMS_PROVIDER", "").strip().upper() or "CUSTOM"
    SMS_USE_GC_NOTIFY = SMS_PROVIDER == "GC_NOTIFY"
    GC_NOTIFY_API_KEY = os.getenv("GC_NOTIFY_API_KEY", "")
    GC_NOTIFY_API_BASE_URL = os.getenv("GC_NOTIFY_API_BASE_URL", "https://api.notification.canada.ca/")
    GC_NOTIFY_SMS_TEMPLATE_ID = os.getenv("GC_NOTIFY_SMS_TEMPLATE_ID", "")
    GC_NOTIFY_EMAIL_TEMPLATE_ID = os.getenv("GC_NOTIFY_EMAIL_TEMPLATE_ID", "")
    SMS_APPOINTMENT_APP_URL = os.getenv("SMS_APPOINTMENT_APP_URL", "")
    APPOINTMENT_APP_URL = os.getenv("APPOINTMENT_APP_URL", "")
    SMS_REMINDER_TEMPLATE = os.getenv("SMS_REMINDER_TEMPLATE", "")
    SMS_CHECKIN_CONFIRMATION_TEMPLATE = os.getenv("SMS_CHECKIN_CONFIRMATION_TEMPLATE", "")

    EMAIL_PROVIDER = os.getenv("EMAIL_PROVIDER", "GC_NOTIFY").strip().upper()
    CHES_SSO_TOKEN_URL = os.getenv("CHES_SSO_TOKEN_URL", "")
    CHES_SSO_CLIENT_ID = os.getenv("CHES_SSO_CLIENT_ID", "")
    CHES_SSO_CLIENT_SECRET = os.getenv("CHES_SSO_CLIENT_SECRET", "")
    CHES_POST_EMAIL_ENDPOINT = os.getenv("CHES_POST_EMAIL_ENDPOINT", "")
    CHES_EMAIL_FROM_ID = os.getenv("CHES_EMAIL_FROM_ID", "")

    WSGI_DEBUG = os.getenv("WSGI_DEBUG", "true").lower() in {"1", "true", "yes", "on"}
    WSGI_HOST = os.getenv("WSGI_HOST", "0.0.0.0")
    WSGI_PORT = int(os.getenv("WSGI_PORT", "5002"))
    WSGI_USE_RELOADER = os.getenv("WSGI_USE_RELOADER", "false").lower() in {"1", "true", "yes", "on"}


class DevConfig(_Config):  # pylint: disable=too-few-public-methods
    """Development configuration."""

    DEBUG = True


class TestConfig(_Config):  # pylint: disable=too-few-public-methods
    """Testing configuration."""

    DEBUG = True
    TESTING = True


class ProdConfig(_Config):  # pylint: disable=too-few-public-methods
    """Production configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        SECRET_KEY = os.urandom(24)
        print("WARNING: SECRET_KEY being set as a one-shot", file=sys.stderr)
