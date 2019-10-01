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
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True,
    DEBUG = True
    LOGGING_LOCATION = "logs/qsystem.log"
    LOGGING_LEVEL = DEBUG
    LOGGING_FORMAT = '[%(asctime)s.%(msecs)03d] %(levelname)-8s (%(name)s) <%(module)s.py>.%(funcName)s: %(message)s'
    LOG_ENABLE = (os.getenv("LOG_ENABLE","FALSE")).upper() == "TRUE"
    PRINT_ENABLE = (os.getenv("PRINT_ENABLE","FALSE")).upper() == "TRUE"

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

    DB_LONG_RUNNING_QUERY = float(os.getenv("DATABASE_LONG_RUNNING_QUERY", '0.5'))

    DB_ENGINE = os.getenv('DATABASE_ENGINE', '')
    DB_USER = os.getenv('DATABASE_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD','')
    DB_NAME = os.getenv('DATABASE_NAME','')
    DB_HOST = os.getenv('DATABASE_HOST','')
    DB_PORT = os.getenv('DATABASE_PORT','')
    DB_TIMEOUT_STRING = os.getenv('DATABASE_TIMEOUT_STRING', '')
    SQLALCHEMY_DATABASE_URI = '{engine}://{user}:{password}@{host}:{port}/{name}{timeout}'.format(
        engine=DB_ENGINE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        name=DB_NAME,
        timeout=DB_TIMEOUT_STRING
    )

    SQLALCHEMY_DATABASE_URI_DISPLAY = '{engine}://{user}:<password>@{host}:{port}/{name}{timeout}'.format(
        engine=DB_ENGINE,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT,
        name=DB_NAME,
        timeout=DB_TIMEOUT_STRING
    )

    #  Get SQLAlchemy environment variables.
    pool_size = int(os.getenv('SQLALCHEMY_POOL_SIZE', '9'))
    max_overflow = int(os.getenv('SQLALCHEMY_MAX_OVERFLOW', '18'))

    #  Try to set some options to avoid long delays.
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size' : pool_size,
        'max_overflow' : max_overflow,
        'pool_pre_ping' : False
    }

    #  Set echo appropriately.
    if (os.getenv('SQLALCHEMY_ECHO', "False")).upper() == "TRUE":
        SQLALCHEMY_ECHO=True
    else:
        SQLALCHEMY_ECHO=False

    THEQ_FEEDBACK = (os.getenv('THEQ_FEEDBACK','')).upper().replace(" ","").split(",")
    SLACK_URL = os.getenv('SLACK_URL', '')
    ROCKET_CHAT_URL = os.getenv('ROCKET_CHAT_URL')
    SERVICENOW_INSTANCE = os.getenv('SERVICENOW_INSTANCE', '')
    SERVICENOW_USER = os.getenv('SERVICENOW_USER', '')
    SERVICENOW_PASSWORD = os.getenv('SERVICENOW_PASSWORD', '')
    SERVICENOW_TABLE = os.getenv('SERVICENOW_TABLE', '')
    SERVICENOW_TENANT = os.getenv('SERVICENOW_TENANT', '')
    SERVICENOW_ASSIGN_GROUP = os.getenv('SERVICENOW_ASSIGN_GROUP', '')

    VIDEO_PATH = os.getenv('VIDEO_PATH', '')
    BACK_OFFICE_DISPLAY = os.getenv("BACK_OFFICE_DISPLAY", "BackOffice")

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
    SECRET_KEY = "pancakes"
    LOCALHOST_DB_IP = "127.0.0.1"

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    REDIS_DEBUG = True
    TESTING = False
    ENV = 'dev'

    USE_HTTPS = True
    PREFERRED_URL_SCHEME = 'https'

class TestConfig(BaseConfig):
    DEBUG = True
    REDIS_DEBUG = True
    TESTING = False
    ENV = 'test'

    USE_HTTPS = True
    PREFERRED_URL_SCHEME = 'https'

class ProductionConfig(BaseConfig):
    DEBUG = True
    REDIS_DEBUG = True
    TESTING = False
    ENV = 'production'

    USE_HTTPS = True
    PREFERRED_URL_SCHEME = 'https'

def configure_app(app):
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)
    print_flag = app.config['PRINT_ENABLE']

    #  See if any logging is wanted.
    if app.config['LOG_ENABLE']:

        #  Get list of available loggers.
        if False:
            print("==> List of available loggers")
            for name in logging.root.manager.loggerDict:
                print("    --> Logger name: " + name)

        # Configure logging for the app.
        if print_flag:
            print("==> Setting up logging")
        location = app.config['LOGGING_LOCATION']
        formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
        handler = logging.FileHandler(location)
        handler.setFormatter(formatter)
        string_level = os.getenv('LOG_BASIC', "")
        msg_level = max(logging.DEBUG, debug_string_to_debug_level(string_level))
        if print_flag:
            print("    --> Setting logging for default app.logger; string_level: " + string_level + "; msg_level: " + str(msg_level))
        app.logger.setLevel(msg_level)
        app.logger.addHandler(handler)

        #  Configure logging for all other loggers.
        setup_logger(print_flag, location, 'asyncio', 'LOG_ASYNCIO', formatter)
        setup_logger(print_flag, location, 'concurrent', 'LOG_CONCURRENT', formatter)
        setup_logger(print_flag, location, 'flask_caching', 'LOG_FLASK_CACHING', formatter)
        setup_logger(print_flag, location, 'flask_cors', 'LOG_FLASK_CORS', formatter)
        setup_logger(print_flag, location, 'flask_restplus', 'LOG_FLASK_RESTPLUS', formatter)
        setup_logger(print_flag, location, 'gunicorn', 'LOG_GUNICORN', formatter)
        setup_logger(print_flag, location, 'gunicorn.access', 'LOG_GUNICORN', formatter)
        setup_logger(print_flag, location, 'psycopg2', 'LOG_PSYCOPG2', formatter)
        setup_logger(print_flag, location, 'requests', 'LOG_REQUESTS', formatter)
        setup_logger(print_flag, location, 'sqlalchemy', 'LOG_SQLALCHEMY', formatter)
        setup_logger(print_flag, location, 'sqlalchemy.orm', 'LOG_SQLALCHEMY_ORM', formatter)
        setup_logger(print_flag, location, 'urllib3', 'LOG_URLLIB3', formatter)

def configure_engineio_socketio(app):

    #  See if any logging is wanted.
    print_flag = app.config['PRINT_ENABLE']
    if app.config['LOG_ENABLE']:
        if print_flag:
            print("==> Setting up engionio and socketio")
        location = app.config['LOGGING_LOCATION']
        formatter = logging.Formatter(app.config['LOGGING_FORMAT'])

        #  Set up logging for last two loggers.
        setup_logger(print_flag, location, 'engineio', 'LOG_ENGINEIO', formatter)
        setup_logger(print_flag, location, 'socketio', 'LOG_SOCKETIO', formatter)

def setup_logger(print_flag, location, log_name, config_name, formatter):

    #  Translate the logging level.
    string_level = os.getenv(config_name, "")
    msg_level = debug_string_to_debug_level(string_level)
    if print_flag:
        print("    --> Setting logging for " + log_name + "; string_level: " + string_level + "; msg_level: " + str(msg_level))

    #  Take action depending on the level.
    if msg_level == -10:
        if print_flag:
            print("    --> " + config_name + " env var not present.  Logger " + log_name + " logging not set up")
    elif msg_level == -20:
        if print_flag:
            print("    --> " + config_name + " env var value '" + string_level + \
                  "' invalid.  Logger " + log_name + " logging not set up")
    else:

        #  All OK.  Set up logging options
        log_file_handler = logging.FileHandler(location)
        log_file_handler.setFormatter(formatter)
        log_stream_handler = logging.StreamHandler()
        log_stream_handler.setFormatter(formatter)
        module_logger = logging.getLogger(log_name)
        module_logger.setLevel(msg_level)
        module_logger.addHandler(log_file_handler)
        module_logger.addHandler(log_stream_handler)

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
