import logging
import socket
import time
import traceback
import datetime

from config import configure_app
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

import sys

# from pprint import pprint

application = Flask(__name__, instance_relative_config=True)

# Make sure we 404 when the trailing slash is not present on ALL routes
application.url_map.strict_slashes = True
configure_app(application)

db = SQLAlchemy(application, engine_options={
    'pool_size' : 15,
    #'timeout' : 10,
    'pool_pre_ping' : True,
    'echo' : 'debug',
    'echo_pool' : 'debug'
})
# db = SQLAlchemy(application)
db.init_app(application)

logging.getLogger('sqlalchemy.engine').info(">>> This is a test info message")
logging.getLogger('sqlalchemy.pool').error(">>> This is a test error message")

# print("==> Loggers")
# for name in logging.root.manager.loggerDict:
#     print("    --> Logger name: " + name)

# print("==> DB engine settings:")
# print("    --> pool_size = {}".format(db.engine.pool.size()))
# print("    --> pool_pre_ping = " + str(db.engine.pool._pre_ping))
# for attr in dir(db.engine.connect):
#     print("db.engine.connect.%s = %r" % (attr, getattr(db.engine.connect, attr)))

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(application)

ma = Marshmallow(application)

socketio = SocketIO(logger=True, engineio_logger=True)

if application.config['ACTIVE_MQ_URL'] is not None:
    socketio.init_app(application, async_mode='eventlet', message_queue=application.config['ACTIVE_MQ_URL'], path='/api/v1/socket.io')
else:
    socketio.init_app(application, path='/api/v1/socket.io')

# Set socket logging
logging.getLogger('socketio').setLevel(application.config['LOG_SOCKETIO'])
logging.getLogger('engineio').setLevel(application.config['LOG_ENGINEIO'])

if application.config['CORS_ALLOWED_ORIGINS'] is not None:
    CORS(application, supports_credentials=True, origins=application.config['CORS_ALLOWED_ORIGINS'])

api = Api(application, prefix='/api/v1', doc='/api/v1/')

#  For some strange, and as yet unknown reason, the following initialization
#  must be done, or the front end queue isn't updated properly in IE browsers.
from app.patches.flask_oidc_patched import OpenIDConnect
oidc = OpenIDConnect(application)

from app import admin

flask_admin = Admin(application, name='Admin Console', template_mode='bootstrap3', index_view=admin.HomeView())

flask_admin.add_view(admin.ChannelModelView)
flask_admin.add_view(admin.CounterModelView)
flask_admin.add_view(admin.CSRModelView)
flask_admin.add_view(admin.InvigilatorModelView)
flask_admin.add_view(admin.OfficeModelView)
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

logger = logging.getLogger("myapp.sqltime")
logger.setLevel(logging.DEBUG)

def api_call_with_retry(f, max_time=15000, max_tries=12, delay_first=100, delay_start=200, delay_mult=1.5):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        #  Initialize variables
        current_try = 1
        current_delay = 0
        total_delay = 0
        time_start = datetime.datetime.now()
        time_current = time_start
        time_save = time_current

        while (current_try <= max_tries) and (total_delay <= max_time):

            print("==> api_call_with_retry: Try #: " + str(current_try) + "; time: " + str(time_current))
            print("    --> delay:   " + str(current_delay) + "; total delay: " + str(total_delay))
            print("    --> elapsed: " + str(time_current - time_save) + "; total elapsed: " + \
                  str(time_current - time_start))

            try:
                return f(*args, **kwargs)
            except SQLAlchemyError as err:
                if current_try < max_tries:
                    time_db_before = datetime.datetime.now()
                    db.session.rollback()
                    time_db_after = datetime.datetime.now()
                    print("        --> SQLAlchemyError: " + str(datetime.datetime.now()))
                    print("        --> Message:         " + str(err))
                    print("        --> rollback time:   " + str(time_db_after - time_db_before))
                    time_current = time_db_after
                else:
                    raise

            #  Update variables.
            if current_try == 1:
                current_delay = delay_first
            elif current_try == 2:
                current_delay = delay_start
            else:
                current_delay = current_delay * delay_mult

            #  Update variables.
            current_try += 1
            total_delay = total_delay + current_delay

            #  Sleep a bit.
            time.sleep(current_delay / 1000.0)

            #  Update more variables.
            time_save = time_current
            time_current = datetime.datetime.now()

    return decorated_function

import app.resources.theq.categories
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

    if total > 0.2:
        logger.debug("Long running Query (%s s): %s" % (total, statement))
        logger.debug("Parameters: %s", parameters)


@application.after_request
def apply_header(response):
    response.headers["X-Node-Hostname"] = hostname
    return response
