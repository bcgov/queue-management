import datetime
import logging
import socket
import time
import traceback

from config import configure_app
from flask import Flask, g, session
from flask_caching import Cache
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import AuthError

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

application = Flask(__name__, instance_relative_config=True)

#Make sure we 404 when the trailing slash is not present on ALL routes
application.url_map.strict_slashes = True
configure_app(application)

db = SQLAlchemy(application)
db.init_app(application)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(application)

ma = Marshmallow(application)

socketio = SocketIO(engineio_logger=True)

if application.config['ACTIVE_MQ_URL'] != None:
    socketio.init_app(application, async_mode='eventlet', message_queue=application.config['ACTIVE_MQ_URL'], path='/api/v1/socket.io')
else:  
    socketio.init_app(application, path='/api/v1/socket.io')

if application.config['CORS_ALLOWED_ORIGINS'] != None:
    CORS(application, supports_credentials=True, origins=application.config['CORS_ALLOWED_ORIGINS'])

api = Api(application, prefix='/api/v1', doc='/api/v1/')

from app.patches.flask_oidc_patched import OpenIDConnect
oidc = OpenIDConnect(application)

logging.basicConfig(format=application.config['LOGGING_FORMAT'], level=logging.INFO)
logger = logging.getLogger("myapp.sqltime")
logger.setLevel(logging.DEBUG)

def api_call_with_retry(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        attempts = 3

        while attempts > 0:
            attempts -= 1
            try:
                return f(*args, **kwargs)
            except SQLAlchemyError as err:
                if attempts > 0:
                    db.session.rollback()
                else:
                    raise

    return decorated_function

import app.resources.categories
import app.resources.channels
import app.resources.citizen.citizen_add_to_queue
import app.resources.citizen.citizen_begin_service
import app.resources.citizen.citizen_detail
import app.resources.citizen.citizen_finish_service
import app.resources.citizen.citizen_generic_invite
import app.resources.citizen.citizen_left
import app.resources.citizen.citizen_list
import app.resources.citizen.citizen_place_on_hold
import app.resources.citizen.citizen_service_requests
import app.resources.citizen.citizen_specific_invite
import app.resources.health
import app.resources.services
import app.resources.service_requests_list
import app.resources.service_requests_detail
import app.resources.slack
import app.resources.websocket

#Hostname for debug puposes
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
