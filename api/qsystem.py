import datetime
import logging
from flask import Flask, g, session
from flask_cors import CORS
from flask_login import LoginManager, current_user
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from config import configure_app

db = SQLAlchemy()

application = Flask(__name__, instance_relative_config=True)

#Make sure we 404 when the trailing slash is not present on ALL routes
application.url_map.strict_slashes = True

configure_app(application)
socketio = SocketIO(engineio_logger=True)
socketio.init_app(application, async_mode='eventlet', message_queue=application.config['REDIS_QUEUE_URL'])
db.init_app(application)

CORS(application, supports_credentials=True, origins=application.config['CORS_ALLOWED_ORIGINS'])

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'login'

api = Api(application, prefix='/api/v1', doc='/')

logging.basicConfig(format=application.config['LOGGING_FORMAT'], level=logging.INFO)

import app.resources.authentication
import app.resources.clients
import app.resources.health
import app.resources.notes
import app.resources.offices
import app.resources.users
import app.resources.websocket
