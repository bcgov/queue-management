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
"""All of the configuration for the service is captured here. All items are loaded, or have Constants defined here that are loaded into the Flask configuration. All modules and lookups get their configuration from the Flask config, rather than reading environment variables directly or by accessing this configuration directly.
"""

import os
import sys

from dotenv import find_dotenv, load_dotenv

# this will load all the envars from a .env file located in the project root (api)
load_dotenv(find_dotenv())

CONFIGURATION = {
    'development': 'config.DevConfig',
    'testing': 'config.TestConfig',
    'production': 'config.ProdConfig',
    'default': 'config.ProdConfig'
}


def get_named_config(config_name: str = 'production'):
    """Return the configuration object based on the name

    :raise: KeyError: if an unknown configuration is requested
    """
    if config_name in ['production', 'staging', 'default']:
        config = ProdConfig()
    elif config_name == 'testing':
        config = TestConfig()
    elif config_name == 'development':
        config = DevConfig()
    else:
        raise KeyError(f"Unknown configuration '{config_name}'")
    return config


class _Config(object):  # pylint: disable=too-few-public-methods
    """Base class configuration that should set reasonable defaults for all the other configurations. """
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = 'a_secret'
    TESTING = False
    DEBUG = True

    OIDC_PROVIDER_TOKEN_URL = os.getenv('OIDC_PROVIDER_TOKEN_URL', None)
    SERVICE_ACCOUNT_ID = os.getenv('SERVICE_ACCOUNT_ID', None)
    SERVICE_ACCOUNT_SECRET = os.getenv('SERVICE_ACCOUNT_SECRET', None)
    REMINDER_ENDPOINT = os.getenv('REMINDER_ENDPOINT', None)

    # Email variables
    # MAIL_SERVER = os.getenv('MAIL_SERVER', 'apps.smtp.gov.bc.ca')
    # MAIL_PORT = os.getenv('MAIL_PORT', '25')
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = False
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME', None)
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', None)
    MAIL_FROM_ID = os.getenv('MAIL_FROM_ID', 'donotreply@gov.bc.ca')

    # Email variables
    EMAIL_APPOINTMENT_APP_URL = os.getenv('EMAIL_APPOINTMENT_APP_URL', None)

    # CHES variables
    CHES_SSO_TOKEN_URL = os.getenv('CHES_SSO_TOKEN_URL', None)
    CHES_SSO_CLIENT_ID = os.getenv('CHES_SSO_CLIENT_ID', None)
    CHES_SSO_CLIENT_SECRET = os.getenv('CHES_SSO_CLIENT_SECRET', None)
    CHES_POST_EMAIL_ENDPOINT = os.getenv('CHES_POST_EMAIL_ENDPOINT', None)

    MAX_EMAIL_PER_BATCH = int(os.getenv('MAX_EMAIL_PER_BATCH', 30))


class DevConfig(_Config):  # pylint: disable=too-few-public-methods
    TESTING = False
    DEBUG = True


class TestConfig(_Config):  # pylint: disable=too-few-public-methods
    """In support of testing only used by the py.test suite."""
    DEBUG = True
    TESTING = True


class ProdConfig(_Config):  # pylint: disable=too-few-public-methods
    """Production environment configuration."""

    SECRET_KEY = os.getenv('SECRET_KEY', None)

    if not SECRET_KEY:
        SECRET_KEY = os.urandom(24)
        print('WARNING: SECRET_KEY being set as a one-shot', file=sys.stderr)

    TESTING = False
    DEBUG = False
