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
from pprint import pprint
from datetime import datetime
from flask import request, g
from flask_restx import Resource
from qsystem import api, api_call_with_retry, db, socketio, my_print
from app.models.theq import Citizen, CSR, Counter, Office, CitizenState
from marshmallow import ValidationError
from app.schemas.theq import CitizenSchema
from sqlalchemy import exc
from app.utilities.snowplow import SnowPlow
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt
from app.utilities.email import send_email, generate_ches_token, get_walkin_reminder_email_contents
from app.utilities.sms import send_walkin_reminder_sms

@api.route("/citizen/all-walkin/<string:id>/", methods=["GET"])
class WalkinDetail(Resource):

    citizen_schema = CitizenSchema()
    citizens_schema = CitizenSchema(many=True)

    def get(self, id):
        try:
            import logging
            logging.info('{}*****!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*****'.format(id))
            citizen = Citizen.query.filter_by(walkin_unique_id=id).join(CitizenState)\
                                            .filter(CitizenState.cs_state_name == 'Active')\
                                            .order_by(Citizen.citizen_id.desc()).first()
            if citizen:
                time_now = datetime.utcnow()
                get_all_walkin = Citizen.query.filter_by(office_id=citizen.office_id)\
                                                .filter(Citizen.start_time >= citizen.start_time)\
                                                .filter(Citizen.counter_id != None)\
                                                .join(CitizenState)\
                                                .filter(CitizenState.cs_state_name == 'Active')\
                                                .order_by(Citizen.start_time.desc())\
                                                .all()
                # get_all_walkin = Citizen.query.filter_by(office_id=citizen.office_id)\
                #                                 .filter(Citizen.start_time >= citizen.start_time)\
                #                                 .filter(Citizen.start_time <= time_now)\
                #                                 .filter(Citizen.counter_id != None)\
                #                                 .join(CitizenState)\
                #                                 .filter(CitizenState.cs_state_name == 'Active')\
                #                                 .order_by(Citizen.start_time.desc())\
                #                                 .all()
                
                logging.info('{}**********'.format(citizen.start_time))
                result = self.citizens_schema.dump(get_all_walkin)
                return {'citizen': result.data,
                    'errors': result.errors}, 200
            return {}
        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500