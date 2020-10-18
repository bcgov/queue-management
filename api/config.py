import logging
import os
import dotenv
from pprint import pprint

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

    #   Set up miscellaneous environment variables.
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True,
    DEBUG = False

    #   Set up logging
    LOGGING_LEVEL = DEBUG
    LOGGING_FORMAT = '[%(asctime)s] %(levelname)-8s (%(name)s) <%(module)s.py>.%(funcName)s: %(message)s'
    PRINT_ENABLE = (os.getenv("PRINT_ENABLE","FALSE")).upper() == "TRUE"
    PRINT_ENABLE_DEBUG_TYPEERROR = (os.getenv("PRINT_ENABLE_DEBUG_TYPEERROR","FALSE")).upper() == "TRUE"
    SOCKET_STRING = os.getenv('LOG_SOCKETIO', 'WARNING')
    ENGINE_STRING = os.getenv('LOG_ENGINEIO', 'WARNING')

    #   Set up OIDC variables.
    SECRET_KEY = os.getenv('SECRET_KEY')
    OIDC_OPENID_REALM = os.getenv('OIDC_OPENID_REALM','nest')
    OIDC_CLIENT_SECRETS = os.getenv('OIDC_SECRETS_FILE','client_secrets/secrets.json')
    OIDC_USER_INFO_ENABLED = True
    OIDC_SCOPES = ['openid', 'email', 'profile']

    #  Set up session and communication variables.
    REMEMBER_COOKIE_DURATION = 86400
    SESSION_COOKIE_DOMAIN = os.getenv('SERVER_NAME', '')
    if os.getenv('CORS_ALLOWED_ORIGINS', None):
        CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split(',')
    else:
        CORS_ALLOWED_ORIGINS = ["https://" + SESSION_COOKIE_DOMAIN]

    #   Set up RabbitMQ variables.
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


    MARSHMALLOW_SCHEMA_DEFAULT_JIT = "toastedmarshmallow.Jit"
    DB_LONG_RUNNING_QUERY = float(os.getenv("DATABASE_LONG_RUNNING_QUERY", '0.5'))

    DB_ENGINE = os.getenv('DATABASE_ENGINE', '')
    DB_USER = os.getenv('DATABASE_USERNAME', '')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD','')
    DB_NAME = os.getenv('DATABASE_NAME','')
    DB_HOST = os.getenv('DATABASE_HOST','')
    DB_PORT = os.getenv('DATABASE_PORT','')
    DB_POOL_TIMEOUT = os.getenv('DATABASE_TIMEOUT_STRING', '')
    DB_CONNECT_TIMEOUT = os.getenv('DATABASE_CONNECT_TIMEOUT_STRING', '')

    SQLALCHEMY_DATABASE_URI = '{engine}://{user}:{password}@{host}:{port}/{name}'.format(
        engine=DB_ENGINE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        name=DB_NAME,
    )

    SQLALCHEMY_DATABASE_URI_DISPLAY = '{engine}://{user}:<password>@{host}:{port}/{name}'.format(
        engine=DB_ENGINE,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT,
        name=DB_NAME,
    )

    #  Get SQLAlchemy environment variables.
    pool_size = int(os.getenv('SQLALCHEMY_POOL_SIZE', '9'))
    max_overflow = int(os.getenv('SQLALCHEMY_MAX_OVERFLOW', '18'))
    # db_timeout = int(os.getenv('SQLALCHEMY_TIMEOUT', '10'))

    # Karims settings
    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     'pool_size': pool_size,
    #     'max_overflow': max_overflow,
    #     'pool_pre_ping': True,
    #     'pool_timeout': 5,
    #     'pool_recycle': 3600,
    #     'connect_args': {
    #         'connect_timeout': 3
    #     }
    # }

    #  Try to set some options to avoid long delays.
    # SQLALCHEMY_ENGINE_OPTIONS  = {
    #     'pool_size' : pool_size,
    #     'max_overflow' : max_overflow,
    #     'pool_pre_ping' : True,
    #     'pool_timeout': DB_POOL_TIMEOUT,
    #     'pool_recycle': 3600,
    #     'connect_args': {
    #         'connect_timeout': DB_CONNECT_TIMEOUT,
    #         'options' : '-c statement_timeout=1000'
    #     }
    # }

    #  Get SQLAlchemy environment variables.
    pool_size = int(os.getenv('SQLALCHEMY_POOL_SIZE', '9'))
    pool_timeout_string = os.getenv('SQLALCHEMY_POOL_TIMEOUT', '')
    connect_timeout_string = os.getenv('SQLALCHEMY_CONNECT_TIMEOUT', '')
    max_overflow = int(os.getenv('SQLALCHEMY_MAX_OVERFLOW', '18'))
    pool_pre_ping = (os.getenv('SQLALCHEMY_POOL_PRE_PING', 'False')).upper() == "TRUE"

    #  Try to set some options to avoid long delays.
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': pool_size,
        'max_overflow': max_overflow,
        'pool_pre_ping': pool_pre_ping
    }

    if pool_timeout_string != "":
        pool_timeout = int(pool_timeout_string)
        SQLALCHEMY_ENGINE_OPTIONS['pool_timeout'] = pool_timeout

    if connect_timeout_string != "":
        connect_timeout = int(connect_timeout_string)

        #   Determine which database engine being used, to use correct syntax.
        if "PG8000" in DB_ENGINE.upper():
            SQLALCHEMY_ENGINE_OPTIONS['connect_args'] = {'timeout': connect_timeout}
            # SQLALCHEMY_ENGINE_OPTIONS['connect_args'] = {'timeout': connect_timeout, 'tcp_user_timeout': 500 }
        else:
            # SQLALCHEMY_ENGINE_OPTIONS['connect_args'] = { 'connect_timeout': connect_timeout, 'tcp_user_timeout': 500 }
            SQLALCHEMY_ENGINE_OPTIONS['connect_args'] = {'connect_timeout': connect_timeout}

    print("==> SQLALCHEMY_ENGINE_OPTIONS (Engine: " + DB_ENGINE)
    pprint(SQLALCHEMY_ENGINE_OPTIONS)

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

    APPOINTMENT_LIMIT_DAYS = os.getenv('APPOINTMENT_LIMIT_DAYS', 15)
 

    VIDEO_PATH = os.getenv('VIDEO_PATH', '')
    BACK_OFFICE_DISPLAY = os.getenv("BACK_OFFICE_DISPLAY", "BackOffice")
    RECURRING_FEATURE_FLAG = os.getenv("RECURRING_FEATURE_FLAG", "On")

    MINIO_HOST = os.getenv('MINIO_HOST', 'localhost:9000')
    MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'exams')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minio')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minio1234')
    MINIO_USE_SECURE = os.getenv('MINIO_USE_SECURE', 0)

    #print(parse_dsn(("postgresql://localhost:5000?connect_timeout=10")))
    #quote_ident("connect_timeout", scope)

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
    #CORS_ALLOWED_ORIGINS = ["http://localhost:8080"]
    SQLALCHEMY_ECHO = False
    SECRET_KEY = "pancakes"

    DB_ENGINE = os.getenv('DATABASE_ENGINE', 'postgres')
    DB_USER = os.getenv('DATABASE_USERNAME', 'postgres')
    DB_PASSWORD = os.getenv('DATABASE_PASSWORD', 'root')
    DB_NAME = os.getenv('DATABASE_NAME', 'qsystem')
    DB_HOST = os.getenv('DATABASE_HOST', '127.0.0.1')
    DB_PORT = os.getenv('DATABASE_PORT', '5432')
    SQLALCHEMY_DATABASE_URI = '{engine}://{user}:{password}@{host}:{port}/{name}'.format(
        engine=DB_ENGINE,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        name=DB_NAME
    )
    BCMP_BASE_URL = os.getenv('BCMP_BASE_URL')
    BCMP_AUTH_TOKEN = os.getenv('BCMP_AUTH_TOKEN')

    MINIO_HOST = os.getenv('MINIO_HOST', 'localhost:9000')
    MINIO_BUCKET = os.getenv('MINIO_BUCKET', 'exams')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minio')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minio1234')
    MINIO_USE_SECURE = os.getenv('MINIO_USE_SECURE', 0)


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    REDIS_DEBUG = True
    TESTING = False
    ENV = 'dev'

    # # Only allowed 1 origin, but need to work for
    # # queue-frontend and appointment-frontend
    # CORS_ALLOWED_ORIGINS = ["https://dev-theq.pathfinder.gov.bc.ca/"]

    USE_HTTPS = True
    PREFERRED_URL_SCHEME = 'https'
    BCMP_BASE_URL = os.getenv('BCMP_BASE_URL')
    BCMP_AUTH_TOKEN = os.getenv('BCMP_AUTH_TOKEN')


class TestConfig(BaseConfig):
    DEBUG = True
    REDIS_DEBUG = True
    TESTING = False
    ENV = 'test'

    USE_HTTPS = True
    PREFERRED_URL_SCHEME = 'https'
    BCMP_BASE_URL = os.getenv('BCMP_BASE_URL')
    BCMP_AUTH_TOKEN = os.getenv('BCMP_AUTH_TOKEN')


class ProductionConfig(BaseConfig):
    DEBUG = True
    REDIS_DEBUG = True
    TESTING = False
    ENV = 'production'

    USE_HTTPS = True
    PREFERRED_URL_SCHEME = 'https'
    BCMP_BASE_URL = os.getenv('BCMP_BASE_URL')
    BCMP_AUTH_TOKEN = os.getenv('BCMP_AUTH_TOKEN')


def configure_app(app):

    #  Do basic configuration from config objects and files.
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.cfg', silent=True)

    #   Set up various variables used later.
    app.config['SOCKET_FLAG'] = logging.DEBUG == debug_string_to_debug_level(app.config['SOCKET_STRING'])
    app.config['ENGINE_FLAG'] = logging.DEBUG == debug_string_to_debug_level(app.config['ENGINE_STRING'])

    #   Set up basic logging for the application.
    log_string = os.getenv('LOG_ROOT', "WARNING").upper()
    log_level = debug_string_to_debug_level(log_string)
    logging.basicConfig(format=app.config['LOGGING_FORMAT'], level=log_level)
    temp_logger = logging.getLogger()
    if app.config['PRINT_ENABLE']:
        print("==> Root logger of '" + temp_logger.name + "' set to level: " + log_string)

def configure_logging(app):

    #   Set up defaults.
    print_flag = app.config['PRINT_ENABLE']
    basic_string = os.getenv('LOG_BASIC', "WARNING").upper()
    basic_level = 0
    if basic_string != "DEFAULT":
        basic_level = debug_string_to_debug_level(basic_string)

    if print_flag:
        print("==> List of loggers being specifically set:")
    for name in logging.root.manager.loggerDict:
        env_name = make_env_name(name)
        log_string = os.getenv(env_name, "None")
        if (log_string != "None"):
            if print_flag:
                print("        --> Logger " + name + " set to level = " + log_string)
            module_logger = logging.getLogger(name)
            log_level = debug_string_to_debug_level(log_string)
            module_logger.setLevel(log_level)
        elif (basic_string != "DEFAULT"):
            if print_flag:
                print("        --> Logger " + name + " set to level LOG_BASIC level of " + basic_string)
            module_logger = logging.getLogger(name)
            module_logger.setLevel(basic_level)

    if print_flag:
        print("")

def make_env_name(name):
    return ("LOG_" + name.upper().replace('.', '_'))

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

def debug_level_to_debug_string(debug_level):
    if debug_level == logging.CRITICAL:
        result = "CRITICAL"
    elif debug_level == logging.ERROR:
        result = "ERROR"
    elif debug_level == logging.WARNING:
        result = "WARNING"
    elif debug_level == logging.INFO:
        result = "INFO"
    elif debug_level == logging.DEBUG:
        result = "DEBUG"
    elif debug_level == logging.NOTSET:
        result = "NOTSET"

    return result
