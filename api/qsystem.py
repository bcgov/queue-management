import datetime
import logging
from flask import Flask, g, session
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from config import configure_app
from sqlalchemy.exc import SQLAlchemyError

from app.patches.flask_oidc_patched import OpenIDConnect
from app.exceptions import AuthError

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

application = Flask(__name__, instance_relative_config=True)

#Make sure we 404 when the trailing slash is not present on ALL routes
application.url_map.strict_slashes = True
configure_app(application)

db = SQLAlchemy(application)
db.init_app(application)
sessionmaker = sessionmaker(db.engine)

ma = Marshmallow(application)

socketio = SocketIO(engineio_logger=True)

if application.config['ACTIVE_MQ_URL'] != None:
    socketio.init_app(application, async_mode='eventlet', message_queue=application.config['ACTIVE_MQ_URL'], path='/api/v1/socket.io')
else:  
    socketio.init_app(application, path='/api/v1/socket.io')

CORS(application, supports_credentials=True, origins=application.config['CORS_ALLOWED_ORIGINS'])

api = Api(application, prefix='/api/v1', doc='/api/v1/')

oidc = OpenIDConnect(application)

logging.basicConfig(format=application.config['LOGGING_FORMAT'], level=logging.INFO)

import app.resources.categories
import app.resources.channels
import app.resources.citizens_list
import app.resources.citizens_detail
import app.resources.citizen_left
import app.resources.health
import app.resources.services
import app.resources.service_requests_list
import app.resources.service_requests_detail
import app.resources.slack
import app.resources.websocket

@api.errorhandler(SQLAlchemyError)
def error_handler(e):
    '''Default error handler'''
    print("======================")
    print(e)
    print("======================")
    return {"message": str(e)}, 500

@application.errorhandler(SQLAlchemyError)
def error_handler(e):
    '''Default error handler'''
    print("======================")
    print(e)
    print("======================")
    return "error"

@api.errorhandler(AuthError)
def handle_auth_error(ex):
    # response = jsonify(ex.error)
    # response.status_code = ex.status_code
    # return response, 401
    return {}, 401

@application.errorhandler(AuthError)
def handle_auth_error(ex):
    # response = jsonify(ex.error)
    # response.status_code = ex.status_code
    # return response, 401
    return {}, 401

