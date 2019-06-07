import logging
import os
import dotenv

# Load all the environment variables from a .env file located in some directory above.
dotenv.load_dotenv(dotenv.find_dotenv())

config = {
    "production": "config.ProductionConfig",
    "prod": "config.ProductionConfig",
    "test": "config.TestConfig",
    "development": "config.DevelopmentConfig",
    "dev": "config.DevelopmentConfig",
    "localhost": "config.LocalConfig",
    "default": "config.LocalConfig"
}

class BaseConfig(object):

    def debug_string_to_debug_level(debug_string):
        input_string = debug_string.lower()
        result = -20
        if input_string == 'critical':
            result = logging.CRITICAL
        elif input_string == 'error':
            result = logging.ERROR
        elif input_string == 'warning':
            result = logging.WARNING
        elif input_string == 'info':
            result = logging.INFO
        elif input_string == 'debug':
            result = logging.DEBUG
        elif input_string == 'notset':
            result = logging.NOTSET
        elif input_string == '':
            result = -10

        return result

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True,
    DEBUG = True
    LOGGING_LOCATION = "logs/qsystem.log"
    LOGGING_LEVEL = DEBUG
    LOGGING_FORMAT = '[%(asctime)s.%(msecs)03d] %(levelname)-8s >>> %(name)s %(message)s'

    SECRET_KEY = os.getenv('SECRET_KEY')
    OIDC_OPENID_REALM = os.getenv('OIDC_OPENID_REALM','nest')
    OIDC_CLIENT_SECRETS = os.getenv('OIDC_SECRETS_FILE','client_secrets/secrets.json')
    OIDC_USER_INFO_ENABLED = True
    OIDC_SCOPES = ['openid', 'email', 'profile']

    MARSHMALLOW_SCHEMA_DEFAULT_JIT = "toastedmarshmallow.Jit"

    REMEMBER_COOKIE_DURATION = 86400
    SERVER_NAME = os.getenv('SERVER_NAME', '')
    SESSION_COOKIE_DOMAIN = os.getenv('SERVER_NAME', '')
    CORS_ALLOWED_ORIGINS = ["https://" + SESSION_COOKIE_DOMAIN]

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
    DB_TIMEOUT_STRING = os.getenv('DATABASE_TIMEOUT_STRING', '')
    # SQLALCHEMY_DATABASE_URI = '{engine}://{user}:{password}@{host}:{port}/{name}'.format(
    # SQLALCHEMY_DATABASE_URI = '{engine}://{user}:{password}@{host}:{port}/{name}{timeoutstring}'.format(
    SQLALCHEMY_DATABASE_URI = '{engine}://{user}:{password}@{host}:{port}/{name}'.format(
        engine=DB_ENGINE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        name=DB_NAME,
        timeoutstring=DB_TIMEOUT_STRING
    )
    # Default pool size
    # SQLALCHEMY_POOL_SIZE = 3

    # Some more SQLALCHEMY options
    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     'pool_size' : 13,
    #     'pool_pre_ping': True
    # }

    # Some more SQLALCHEMY options
    # SQLALCHEMY_ENGINE_OPTIONS = { 'poolclass' : NullPool,  }

    #  Print out DB values.
    print("==> Database Values")
    print("    --> DB_ENGINE:      " + DB_ENGINE)
    print("    --> DB_USER:        " + DB_USER)
    print("    --> DB_PASSWORD:    " + DB_PASSWORD)
    print("    --> DB_NAME:        " + DB_NAME)
    print("    --> DB_HOST:        " + DB_HOST)
    print("    --> DB_PORT:        " + DB_PORT)
    print("    --> DB_TOUT_STRING: " + DB_TIMEOUT_STRING)
    print("    --> SQLALCHEMY_DATABASE_URI: " + SQLALCHEMY_DATABASE_URI)

    # print("==> Debug levels:")
    LOG_BASIC = debug_string_to_debug_level(os.getenv("LOG_BASIC", "Debug"))
    # print("    --> LOG_BASIC:               " + os.getenv("LOG_BASIC", "Debug") + "; Value: " + str(LOG_BASIC))
    LOG_ASYNCIO = debug_string_to_debug_level(os.getenv("LOG_ASYNCIO", ""))
    # print("    --> LOG_ASYNCIO:             " + os.getenv("LOG_ASYNCIO", "<None>") + "; Value: " + str(LOG_ASYNCIO))
    LOG_CONCURRENT = debug_string_to_debug_level(os.getenv("LOG_CONCURRENT", ""))
    # print("    --> LOG_CONCURRENT:          " + os.getenv("LOG_CONCURRENT", "<None>") + "; Value: " + str(LOG_CONCURRENT))
    LOG_ENGINEIO = debug_string_to_debug_level(os.getenv("LOG_ENGINEIO", ""))
    # print("    --> LOG_ENGINEIO:            " + os.getenv("LOG_ENGINEIO", "<None>") + "; Value: " + str(LOG_ENGINEIO))
    LOG_FLASK_CACHING = debug_string_to_debug_level(os.getenv("LOG_FLASK_CACHING", ""))
    # print("    --> LOG_FLASK_CACHING:       " + os.getenv("LOG_FLASK_CACHING", "<None>") + "; Value: " + str(LOG_FLASK_CACHING))
    LOG_FLASK_CORS = debug_string_to_debug_level(os.getenv("LOG_FLASK_CORS", ""))
    # print("    --> LOG_FLASK_CORS:          " + os.getenv("LOG_FLASK_CORS", "<None>") + "; Value: " + str(LOG_FLASK_CORS))
    LOG_FLASK_RESTPLUS = debug_string_to_debug_level(os.getenv("LOG_FLASK_RESTPLUS", ""))
    # print("    --> LOG_FLASK_RESTPLUS:      " + os.getenv("LOG_FLASK_RESTPLUS", "<None>") + "; Value: " + str(LOG_FLASK_RESTPLUS))
    LOG_GUNICORN = debug_string_to_debug_level(os.getenv("LOG_GUNICORN", ""))
    # print("    --> LOG_GUNICORN:            " + os.getenv("LOG_GUNICORN", "<None>") + "; Value: " + str(LOG_GUNICORN))
    LOG_PSYCOPG2 = debug_string_to_debug_level(os.getenv("LOG_PSYCOPG2", ""))
    # print("    --> LOG_PSYCOPG2:            " + os.getenv("LOG_PSYCOPG2", "<None>") + "; Value: " + str(LOG_PSYCOPG2))
    LOG_REQUESTS = debug_string_to_debug_level(os.getenv("LOG_REQUESTS", ""))
    # print("    --> LOG_REQUESTS:            " + os.getenv("LOG_REQUESTS", "<None>") + "; Value: " + str(LOG_REQUESTS))
    LOG_SOCKETIO = debug_string_to_debug_level(os.getenv("LOG_SOCKETIO", ""))
    # print("    --> LOG_SOCKETIO2:           " + os.getenv("LOG_SOCKETIO", "<None>") + "; Value: " + str(LOG_SOCKETIO))
    LOG_SQLALCHEMY = debug_string_to_debug_level(os.getenv("LOG_SQLALCHEMY", ""))
    # print("    --> LOG_SQLALCHEMY:          " + os.getenv("LOG_SQLALCHEMY", "<None>") + "; Value: " + str(LOG_SQLALCHEMY))
    LOG_SQLALCHEMY_ORM = debug_string_to_debug_level(os.getenv("LOG_SQLALCHEMY_ORM", ""))
    # print("    --> LOG_SQLALCHEMY_ORM:      " + os.getenv("LOG_SQLALCHEMY_ORM", "<None>") + "; Value: " + str(LOG_SQLALCHEMY_ORM))
    LOG_URLLIB3 = debug_string_to_debug_level(os.getenv("LOG_URLLIB3", ""))
    # print("    --> LOG_URLLIB3:             " + os.getenv("LOG_URLLIB3", "<None>") + "; Value: " + str(LOG_URLLIB3))

    THEQ_FEEDBACK = (os.getenv('THEQ_FEEDBACK','')).upper().replace(" ","").split(",")
    SLACK_URL = os.getenv('SLACK_URL', '')
    ROCKET_CHAT_URL = os.getenv('ROCKET_CHAT_URL')
    SERVICENOW_INSTANCE = os.getenv('SERVICENOW_INSTANCE', '')
    SERVICENOW_USER = os.getenv('SERVICENOW_USER', '')
    SERVICENOW_PASSWORD = os.getenv('SERVICENOW_PASSWORD', '')
    SERVICENOW_TABLE = os.getenv('SERVICENOW_TABLE', '')
    SERVICENOW_TENANT = os.getenv('SERVICENOW_TENANT', '')
    SERVICENOW_ASSIGN_GROUP = os.getenv('SERVICENOW_ASSIGN_GROUP', '')

class LocalConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    ENV = 'dev'

    USE_HTTPS = False
    PREFERRED_URL_SCHEME = 'http'

    ACTIVE_MQ_URL = ''
    #  For running rabbitmq locally, use the line below.
    # ACTIVE_MQ_URL = 'amqp://guest:guest@localhost:5672'

    SERVER_NAME = None
    SESSION_COOKIE_DOMAIN = None
    CORS_ALLOWED_ORIGINS = ["http://localhost:8080"]
    SQLALCHEMY_ECHO = False
    # SQLALCHEMY_POOL_SIZE = 12
    SECRET_KEY = "pancakes"
    LOCALHOST_DB_IP = "127.0.0.1"

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    REDIS_DEBUG = True
    TESTING = False
    ENV = 'dev'

    USE_HTTPS = True
    PREFERRED_URL_SCHEME = 'https'

    if os.getenv('SQLALCHEMY_ECHO', "False") == "True":
        SQLALCHEMY_ECHO=True
    else:
        SQLALCHEMY_ECHO=False

class TestConfig(BaseConfig):
    DEBUG = True
    REDIS_DEBUG = True
    TESTING = False
    ENV = 'test'

    USE_HTTPS = True
    PREFERRED_URL_SCHEME = 'https'

    if os.getenv('SQLALCHEMY_ECHO', "False") == "True":
        SQLALCHEMY_ECHO=True
    else:
        SQLALCHEMY_ECHO=False

class ProductionConfig(BaseConfig):
    DEBUG = True
    REDIS_DEBUG = True
    TESTING = False
    ENV = 'production'

    USE_HTTPS = True
    PREFERRED_URL_SCHEME = 'https'

    if os.getenv('SQLALCHEMY_ECHO', "False") == "True":
        SQLALCHEMY_ECHO=True
    else:
        SQLALCHEMY_ECHO=False

def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)

    # Configure logging
    print("==> Logging levels")

    level = app.config['LOG_BASIC']
    if level >= 0:
        logging.basicConfig(format=app.config['LOGGING_FORMAT'], level=level, datefmt='%Y-%m-%d %H:%M:%S')
        print("    --> basicConfig:    " + str(level))

    set_log_level(app, 'LOG_ASYNCIO', 'asyncio')
    set_log_level(app, 'LOG_CONCURRENT', 'concurrent')
    set_log_level(app, 'LOG_ENGINEIO', 'engineio')
    set_log_level(app, 'LOG_FLASK_CACHING', 'flask_caching')
    set_log_level(app, 'LOG_FLASK_CORS', 'flask_caching')
    set_log_level(app, 'LOG_FLASK_RESTPLUS', 'flask_restplus')
    set_log_level(app, 'LOG_GUNICORN', 'gunicorn')
    set_log_level(app, 'LOG_PSYCOPG2', 'psycopg2')
    set_log_level(app, 'LOG_REQUESTS', 'requests')
    set_log_level(app, 'LOG_SOCKETIO', 'socketio')
    set_log_level(app, 'LOG_SQLALCHEMY', 'sqlalchemy')
    set_log_level(app, 'LOG_SQLALCHEMY_ORM', 'sqlalchemy.orm')
    set_log_level(app, 'LOG_URLLIB3', 'urllib3')

def set_log_level(app, config_name, log_name):

    level = app.config[config_name]
    if level >= 0:
        logging.getLogger(log_name).setLevel(level)
        print("    --> " + config_name + ": " + str(level))
    elif level == -10:
        print("    --> " + config_name + " env var not present.  Logger " + log_name + " logging level not set")
    elif level == -20:
        print("    --> " + config_name + " env var value invalid.  Logger " + log_name + " logging level not set")

    # formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    # handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    # handler.setLevel(app.config['LOGGING_LEVEL'])
    # handler.setFormatter(formatter)
    # app.logger.addHandler(handler)
