import logging
import socket
import time
import traceback
import os

from config import configure_app, configure_engineio_socketio, debug_string_to_debug_level
from flask import Flask
from flask_admin import Admin
from flask_caching import Cache
from flask_compress import Compress
from flask_cors import CORS
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions import AuthError
from sqlalchemy import event
from sqlalchemy.engine import Engine

import datetime

def my_print(string):
    if print_flag:
        print(string)

application = Flask(__name__, instance_relative_config=True)

# Make sure we 404 when the trailing slash is not present on ALL routes
application.url_map.strict_slashes = True
configure_app(application)

db = SQLAlchemy(application)
db.init_app(application)

query_limit = application.config['DB_LONG_RUNNING_QUERY']

#  See whether options took.
print_flag = application.config['PRINT_ENABLE']
if print_flag:
     print("==> DB Engine options")
     print("    --> pool size:    " + str(db.engine.pool.size()))
     print("    --> max overflow: " + str(db.engine.pool._max_overflow))
     print("    --> echo:         " + str(db.engine.echo))
     print("    --> pre ping:     " + str(db.engine.pool._pre_ping))
     print("    --> Database URI: " + application.config['SQLALCHEMY_DATABASE_URI_DISPLAY'])

#  Debugging the engine in general.
if False:
    print("==> All DB Engine options")
    for attr in dir(db.engine):
        print("    --> db.engine." + attr + " = " + str(getattr(db.engine, attr)))
        # print("db.engine.%s = %s") % (attr, getattr(db.engine, attr))

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(application)

ma = Marshmallow(application)

#  NOTE!!  Log levels for socketio and engineio set in configure_app
log_enable_flag = application.config['LOG_ENABLE']
if log_enable_flag:
    socket_flag = logging.DEBUG == debug_string_to_debug_level(os.getenv('LOG_SOCKETIO', ''))
    engine_flag = logging.DEBUG == debug_string_to_debug_level(os.getenv('LOG_ENGINEIO', ''))
else:
    socket_flag = False
    engine_flag = False

my_print("==> Log / Socket / Engine flags")
my_print("    --> log:    " + str(log_enable_flag))
my_print("    --> socket: " + os.getenv('LOG_SOCKETIO', '') + '; flag: ' + str(socket_flag))
my_print("    --> engine: " + os.getenv('LOG_ENGINEIO', '') + '; flag: ' + str(engine_flag))

socketio = SocketIO(logger=socket_flag, engineio_logger=engine_flag,
                    cors_allowed_origins=application.config['CORS_ALLOWED_ORIGINS'])

if application.config['ACTIVE_MQ_URL'] is not None:
    socketio.init_app(application, async_mode='eventlet',
                      message_queue=application.config['ACTIVE_MQ_URL'],
                      path='/api/v1/socket.io')
else:
    socketio.init_app(application, path='/api/v1/socket.io')

configure_engineio_socketio(application)

if application.config['CORS_ALLOWED_ORIGINS'] is not None:
    CORS(application, supports_credentials=True, origins=application.config['CORS_ALLOWED_ORIGINS'])

api = Api(application, prefix='/api/v1', doc='/api/v1/')

from flask_oidc import OpenIDConnect
oidc = OpenIDConnect(application)

from app import admin

flask_admin = Admin(application, name='Admin Console', template_mode='bootstrap3', index_view=admin.HomeView())

flask_admin.add_view(admin.ChannelModelView)
flask_admin.add_view(admin.CounterModelView)
flask_admin.add_view(admin.CSRModelView)
flask_admin.add_view(admin.CSRGAModelView)
flask_admin.add_view(admin.InvigilatorModelView)
flask_admin.add_view(admin.OfficeModelView)
flask_admin.add_view(admin.OfficeGAModelView)
flask_admin.add_view(admin.RoleModelView)
flask_admin.add_view(admin.ServiceModelView)
flask_admin.add_view(admin.SmartBoardModelView)
flask_admin.add_view(admin.RoomModelView)
flask_admin.add_view(admin.ExamTypeModelView)
flask_admin.add_link(admin.LoginMenuLink(name='Login', category='', url="/api/v1/login/"))
flask_admin.add_link(admin.LogoutMenuLink(name='Logout', category='', url="/api/v1/logout/"))

login_manager = LoginManager()
login_manager.init_app(application)
import app.auth

compress = Compress()
compress.init_app(application)

logging.basicConfig(format=application.config['LOGGING_FORMAT'], level=logging.WARNING)
logger = logging.getLogger("myapp.sqltime")
logger.setLevel(logging.DEBUG)

def my_print(string):
    if print_flag:
        print(string)

def api_call_with_retry(f, max_time=15000, max_tries=12, delay_first=100, delay_start=200, delay_mult=1.5):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        #  Initialize variables
        parameters = {}
        parameters['current_try'] = 1
        parameters['current_delay'] = 0
        parameters['total_delay'] = 0
        parameters['time_start'] = datetime.datetime.now()
        parameters['time_current'] = parameters['time_start']
        parameters['time_save'] = parameters['time_current']
        parameters['key'] = get_key()

        while (parameters['current_try'] <= max_tries) and (parameters['total_delay'] <= max_time):

            # Determine whether to print debug statements or not.
            print_debug = print_flag or (parameters['current_try'] > 1)

            print_retry_info(print_debug, parameters, f, kwargs)

            try:
                return f(*args, **kwargs)
            except SQLAlchemyError as err:
                print_error_info(print_debug, parameters, err)
                if parameters['current_try'] < max_tries:
                    db.session.rollback()
                    parameters['time_current'] = datetime.datetime.now()
                else:
                    raise

            #  Update variables.
            parameters['current_delay'] = update_delay(parameters['current_delay'], \
                                                       parameters['current_try'], delay_first, \
                                                       delay_start, delay_mult)

            #  Update variables.
            parameters['current_try'] += 1
            parameters['total_delay'] = parameters['total_delay'] + parameters['current_delay']

            #  Sleep a bit.
            time.sleep(parameters['current_delay'] / 1000.0)

            #  Update more variables.
            parameters['time_save'] = parameters['time_current']
            parameters['time_current'] = datetime.datetime.now()

    return decorated_function

def print_retry_info(print_debug, parameters, f, kwargs):

    if print_debug:
        msg = "==> RT K:" + parameters['key'] + "; T:" + str(parameters['current_try']) \
            + "; F:" + str(f) + "; KW:" + str(kwargs) if kwargs is not None else "None"
        print(msg)

def print_error_info(print_debug, parameters, err):
    if print_debug:
        msg = "==> AE K:" + parameters['key'] + "; T:" + str(parameters['current_try']) \
            + "; E:" + str(err).replace("\n", ">").replace("\r", ">")
        print(msg)

        #  Print more info, if the builtins.dict error.
        # if "builtins.dict" in str(err):
        # if "could not connect" in str(err):
        if parameters['current_try'] == 2:
            print("==> TB K:" + parameters['key'] + "; T:" + str(parameters['current_try']))
            traceback.print_tb(err.__traceback__)

def update_delay(current_delay, current_try, delay_first, delay_start, delay_mult):
    if current_try == 1:
        output_delay = delay_first
    elif current_try == 2:
        output_delay = delay_start
    else:
        output_delay = current_delay * delay_mult
    return output_delay

def get_key():
    time_now = datetime.datetime.today()
    alpha = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    char_year = alpha[time_now.year - 2019]
    char_month = alpha[time_now.month - 1]
    char_day = alpha[time_now.day - 1]
    char_hour = alpha[time_now.hour]
    char_minute = alpha[time_now.minute]
    char_ms = str(time_now.microsecond)[:2]
    return char_year + char_month + char_day + char_hour + char_minute + char_ms

import app.resources.theq.categories
import app.resources.theq.upload
import app.resources.theq.channels
import app.resources.theq.citizen.citizen_add_to_queue
import app.resources.theq.citizen.citizen_begin_service
import app.resources.theq.citizen.citizen_detail
import app.resources.theq.citizen.citizen_finish_service
import app.resources.theq.citizen.citizen_generic_invite
import app.resources.theq.citizen.citizen_left
import app.resources.theq.citizen.citizen_list
import app.resources.theq.citizen.citizen_place_on_hold
import app.resources.theq.citizen.citizen_service_requests
import app.resources.theq.citizen.citizen_specific_invite
import app.resources.theq.csrs
import app.resources.theq.csr_states
import app.resources.theq.csr_detail
import app.resources.theq.feedback
import app.resources.theq.health
import app.resources.theq.login
import app.resources.theq.offices
import app.resources.theq.services
import app.resources.theq.service_requests_list
import app.resources.theq.service_requests_detail
import app.resources.theq.smartboard
import app.resources.theq.videofiles
import app.resources.theq.websocket

import app.resources.bookings.appointment.appointment_detail
import app.resources.bookings.appointment.appointment_list
import app.resources.bookings.appointment.appointment_post
import app.resources.bookings.appointment.appointment_put
import app.resources.bookings.appointment.appointment_delete
import app.resources.bookings.booking.booking_delete
import app.resources.bookings.booking.booking_detail
import app.resources.bookings.booking.booking_list
import app.resources.bookings.booking.booking_post
import app.resources.bookings.booking.booking_put
import app.resources.bookings.exam.exam_delete
import app.resources.bookings.exam.exam_detail
import app.resources.bookings.exam.exam_list
import app.resources.bookings.exam.exam_post
import app.resources.bookings.exam.exam_put
import app.resources.bookings.exam.exam_export_list
import app.resources.bookings.invigilator.invigilator_list
import app.resources.bookings.invigilator.invigilator_put
import app.resources.bookings.room.room_list
import app.resources.bookings.exam_type.exam_type_list

# Hostname for debug purposes
hostname = socket.gethostname()


@api.errorhandler(SQLAlchemyError)
def error_handler(e):
    '''Default error handler'''
    print(e)
    return {"message": str(e), "trace": traceback.format_exc()}, 500


@application.errorhandler(SQLAlchemyError)
def error_handler(e):
    '''Default error handler'''
    print(e)
    return "error"


@application.errorhandler(AuthError)
@api.errorhandler(AuthError)
def handle_auth_error(ex):
    return {}, 401


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
                        parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement,
                        parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)

    if total > query_limit:
        logger.debug("Long running Query (%s s): %s" % (total, statement))
        logger.debug("Parameters: %s", parameters)


@application.after_request
def apply_header(response):
    response.headers["X-Node-Hostname"] = hostname
    return response