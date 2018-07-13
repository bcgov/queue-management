import logging
import os

config = {
    "development": "config.DevelopmentConfig",
    "localhost": "config.LocalConfig",
    "default": "config.LocalConfig"
}

class BaseConfig(object):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True,
    DEBUG = True
    LOGGING_LOCATION = "logs/qsystem.log"
    LOGGING_LEVEL = DEBUG
    LOGGING_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'

    SECRET_KEY = os.getenv('SECRET_KEY','d3a728fc-0671-4c08-82fe-602c695450cf')
    OIDC_OPENID_REALM = os.getenv('OIDC_OPENID_REALM','nest')
    OIDC_CLIENT_SECRETS = os.getenv('OIDC_SECRETS_FILE','client_secrets/secrets.json')
    OIDC_USER_INFO_ENABLED = True
    OIDC_SCOPES = ['openid', 'email', 'profile']

class LocalConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    ENV = 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    ACTIVE_MQ_URL = ''      #'amqp://guest:guest@localhost:5672'
    CORS_ALLOWED_ORIGINS = ["http://localhost:8080"]
    SECRET_KEY = 'a9eec0e0-23b7-4788-9a92-318347b9a39f'
    USE_HTTPS = False
    SQLALCHEMY_ECHO = False
    SLACK_URL = os.getenv('SLACK_URL')

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    REDIS_DEBUG = True
    TESTING = False
    ENV = 'dev'
    SECRET_KEY = 'a9eec0e0-23b7-4788-9a92-318347b9a39f'

    SESSION_COOKIE_DOMAIN = '.pathfinder.gov.bc.ca'
    REMEMBER_COOKIE_DURATION = 86400
    USE_HTTPS = True

    CORS_ALLOWED_ORIGINS = [""]

    ACTIVE_MQ_USER = os.getenv('ACTIVE_MQ_USER', '')
    ACTIVE_MQ_PASSWORD = os.getenv('ACTIVE_MQ_PASSWORD', '')
    ACTIVE_MQ_HOST = os.getenv('ACTIVE_MQ_HOST', '')
    ACTIVE_MQ_PORT = os.getenv('ACTIVE_MQ_PORT', '')
    ACTIVE_MQ_URL = 'amqp://{amq_user}:{amq_password}@{amq_host}:{amq_port}'.format(
        amq_user=ACTIVE_MQ_USER,
        amq_password=ACTIVE_MQ_PASSWORD,
        amq_host=ACTIVE_MQ_HOST,
        amq_port=ACTIVE_MQ_PORT
    )

    DB_ENGINE = os.getenv('DATABASE_ENGINE', '')
    DB_USER = os.getenv('DATABASE_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD','')
    DB_NAME = os.getenv('DATABASE_NAME','')
    DB_HOST = os.getenv('DATABASE_HOST','')
    DB_PORT = os.getenv('DATABASE_PORT','')
    SQLALCHEMY_DATABASE_URI = '{engine}://{user}:{password}@{host}:{port}/{name}'.format(
        engine=DB_ENGINE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        name=DB_NAME,
    )

    SLACK_URL = os.getenv('SLACK_URL')

    if os.getenv('SQLALCHEMY_ECHO', "False") == "True":
        SQLALCHEMY_ECHO=True
    else:
        SQLALCHEMY_ECHO=False

def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)

    # Configure logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
