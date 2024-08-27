'''Copyright 2018 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''
import logging
from datetime import datetime, timezone
from flask import request
from flask_restx import Resource
from qsystem import api, api_call_with_retry, db, socketio, my_print
from app.models.theq import Citizen, CSR, Counter, Office
from marshmallow import ValidationError
from app.schemas.theq import CitizenSchema
from sqlalchemy import exc
from app.utilities.snowplow import SnowPlow
from app.utilities.auth_util import Role, get_username
from app.auth.auth import jwt
from app.utilities.email import send_email, get_walkin_reminder_email_contents
from app.utilities.sms import send_walkin_reminder_sms

@api.route("/citizens/<int:id>/", methods=["GET", "PUT"])
class CitizenDetail(Resource):

    citizen_schema = CitizenSchema()

    @jwt.has_one_of_roles([Role.internal_user.value])
    def get(self, id):
        try:
            citizen = Citizen.query.filter_by(citizen_id=id).first()
            citizen_ticket = "None"
            if hasattr(citizen, 'ticket_number'):
                citizen_ticket = str(citizen.ticket_number)
            my_print("==> GET /citizens/" + str(citizen.citizen_id) + '/, Ticket: ' + citizen_ticket)
            result = self.citizen_schema.dump(citizen)
            return {'citizen': result,
                    'errors': self.citizen_schema.validate(citizen)}

        except exc.SQLAlchemyError as exception:
            logging.exception(exception)
            return {'message': 'API is down'}, 500

    @jwt.has_one_of_roles([Role.internal_user.value])
    @api_call_with_retry
    def put(self, id):
        json_data = request.get_json()

        if 'counter_id' not in json_data:
            json_data['counter_id'] = counter_id

        if not json_data:
            return {'message': 'No input data received for updating citizen'}, 400

        csr = CSR.find_by_username(get_username())
        citizen = Citizen.query.filter_by(citizen_id=id).first()
        my_print("==> PUT /citizens/" + str(citizen.citizen_id) + '/, Ticket: ' + str(citizen.ticket_number))
        if not (json_data.get('is_first_reminder', False) or json_data.get('is_second_reminder', False)):
            try:
                citizen = self.citizen_schema.load(json_data, instance=citizen, partial=True)
            except ValidationError as err:
                return {'message': err.messages}, 422
        else:
            try:
                office_obj = Office.find_by_id(citizen.office_id)
                if (citizen.notification_phone):
                    sms_sent = False
                    # code/function call to send sms notification,
                    sms_sent = send_walkin_reminder_sms(citizen, office_obj, request.headers['Authorization'].replace('Bearer ', ''))
                    if (json_data.get('is_first_reminder', False)) and (sms_sent):
                        citizen.reminder_flag = 1
                        citizen.notification_sent_time = datetime.now(timezone.utc)
                    if (json_data.get('is_second_reminder', False)) and (sms_sent):
                        citizen.reminder_flag = 2
                        citizen.notification_sent_time = datetime.now(timezone.utc)
                if (citizen.notification_email):
                    # code/function call to send first email notification,
                    email_sent = False
                    email_sent = get_walkin_reminder_email_contents(citizen, office_obj)
                    if email_sent:
                        send_email(request.headers['Authorization'].replace('Bearer ', ''), *email_sent)
                    if (json_data.get('is_first_reminder', False)) and email_sent:
                        citizen.reminder_flag = 1
                        citizen.notification_sent_time = datetime.now(timezone.utc)
                    if (json_data.get('is_second_reminder', False)) and email_sent:
                        citizen.reminder_flag = 2
                        citizen.notification_sent_time = datetime.now(timezone.utc)
                    
            except ValidationError as err:
                return {'message': err.messages}, 422

        db.session.add(citizen)
        db.session.commit()

        #  If this put request is the result of an appointment checkin, make a Snowplow call.
        if ('snowplow_addcitizen' in json_data) and (json_data['snowplow_addcitizen'] == True):
            SnowPlow.add_citizen(citizen, csr)

        result = self.citizen_schema.dump(citizen)
        citizen = Citizen.query.filter_by(citizen_id=citizen.citizen_id).first()
        socketio.emit('update_active_citizen', result, room=csr.office.office_name)

        return {'citizen': result,
                'errors': self.citizen_schema.validate(citizen)}, 200

try:
    counter = Counter.query.filter(Counter.counter_name=="Counter")[0]
    counter_id = counter.counter_id
#  NOTE!!  There should ONLY be an exception when first building the database
#          from a python3 manage.py db upgrade command.
except:
    counter_id = 1
    logging.exception("==> In citizen_detail.py")
    logging.exception("    --> NOTE!!  You should only see this if doing a 'python3 manage.py db upgrade'")
