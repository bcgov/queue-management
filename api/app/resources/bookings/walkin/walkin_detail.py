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
import pytz
from pprint import pprint
from datetime import datetime, timedelta
from flask import request, g
from flask_restx import Resource
from qsystem import api, api_call_with_retry, db, socketio, my_print
from app.models.theq import Citizen, CSR, Counter, Office, CitizenState, ServiceReq
from app.models.bookings import Appointment
from marshmallow import ValidationError
from app.schemas.theq import CitizenSchema
from app.schemas.bookings import AppointmentSchema
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
    appointment_schema = AppointmentSchema(many=True)

    def get(self, id):
        try:
            citizen = Citizen.query.filter_by(walkin_unique_id=id).join(CitizenState)\
                                            .filter(CitizenState.cs_state_name == 'Active')\
                                            .order_by(Citizen.citizen_id.desc()).first()
            if citizen:
                time_now = datetime.utcnow()
                past_hour = datetime.utcnow() - timedelta(hours=1)
                future_hour = datetime.utcnow() + timedelta(hours=4)
                
                all_citizen_in_q = Citizen.query.filter_by(office_id=citizen.office_id) \
                                                .join(CitizenState)\
                                                .filter(CitizenState.cs_state_name == 'Active')\
                                                .order_by(Citizen.priority) \
                                                .join(Citizen.service_reqs).all()
                # all_citizen_in_q_result = self.citizens_schema.dump(citizens)
                                            # .filter((Appointment.checked_in_time == None)\
                                            # | (Appointment.is_draft != False)\
                                            # | (Appointment.blackout_flag != 'Y'))\
                                            # .order_by(Appointment.start_time)\
                local_past = pytz.utc.localize(past_hour)
                local_future = pytz.utc.localize(future_hour)
                appointments = Appointment.query.filter_by(office_id=citizen.office_id)\
                                            .filter(Appointment.start_time <= local_future)\
                                            .filter(Appointment.start_time >= local_past)\
                                            .filter((Appointment.checked_in_time == None)\
                                            | (Appointment.is_draft != False)\
                                            | (Appointment.blackout_flag != 'Y'))\
                                            .order_by(Appointment.start_time)\
                                            .all()

                # get_all_booked = Citizen.query.filter_by(office_id=citizen.office_id)\
                #                             .filter(Citizen.start_time <= future_hour)\
                #                             .filter(Citizen.start_time >= past_hour)\
                #                             .filter(Citizen.counter_id == None)\
                #                             .join(CitizenState)\
                #                             .filter((CitizenState.cs_state_name == 'Active')\
                #                             | (CitizenState.cs_state_name == 'Appointment booked'))\
                #                             .join(Appointment)\
                #                              .filter((Appointment.checked_in_time == None)\
                #                             | (Appointment.is_draft != False)\
                #                             | (Appointment.blackout_flag != 'Y'))\
                #                             .order_by(Appointment.start_time)\
                #                             .order_by(Citizen.start_time)\
                #                             .all()

                # TODO: ALL COMMENTED THINGS BELOW
                # result = self.citizens_schema.dump(all_appointment)
                # END
                import logging
                result_in_Q = self.citizens_schema.dump(all_citizen_in_q)
                # logging.info('{}++####result in q----->>>>'.format(result_in_Q))
                # result_in_Book = self.citizens_schema.dump(get_all_booked)
                result_in_Book = self.appointment_schema.dump(appointments)
                logging.info('{}+@@@@@resilt in book--->>>>>'.format(result_in_Book))
                result = result_in_Q + result_in_Book
                # res_list = result_in_Book
                # logging.info('{}+!!!!!!!!!!!!res'.format(result))
                res_list = []
                for each in result:
                    if bool(each.get('service_reqs', False)):
                        for i in each['service_reqs']:
                            served_period = sorted(i['periods'], key= lambda x:x['period_id'], reverse=True)[0]
                            if served_period:
                                if served_period['ps']['ps_name'] == 'Being Served':
                                    each['service_begin_seconds'] = (datetime.utcnow()-datetime.strptime(served_period['time_start'], '%Y-%m-%dT%H:%M:%S.%f')).total_seconds()
                                    shall_append = True
                                    break
                                    res_list.append(each)
                                if (not (served_period['time_end']) and (served_period['ps']['ps_name'] == 'Waiting')):
                                    res_list.append(each)
                                    break
                return {'citizen': result_in_Book}, 200
            return {}
        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500

# get_all_walkin = Citizen.query.filter_by(office_id=citizen.office_id)\
#                                 .filter(Citizen.start_time <= citizen.start_time)\
#                                 .filter(Citizen.start_time > citizen.start_time - timedelta(1))\
#                                 .join(CitizenState)\
#                                 .filter((CitizenState.cs_state_name == 'Active')\
#                                 | (CitizenState.cs_state_name == 'Appointment booked'))\
#                                 .order_by(Citizen.start_time)\
#                                 .all()
# get_all_walkin = Citizen.query.filter_by(office_id=citizen.office_id)\
#                                 .filter(Citizen.start_time <= future_hour)\
#                                 .filter(Citizen.start_time >= past_hour)\
#                                 .filter(Citizen.counter_id == None)\
#                                 .join(CitizenState)\
#                                 .filter((CitizenState.cs_state_name == 'Active')\
#                                 | (CitizenState.cs_state_name == 'Appointment booked'))\
#                                 .order_by(Citizen.start_time)\
#                                 .all()
# get_all_booked = Citizen.query.filter_by(office_id=citizen.office_id)\
#                                 .filter(Citizen.start_time <= citizen.start_time + timedelta(hours=3))\
#                                 .filter(Citizen.start_time >= citizen.start_time - timedelta(hours=1))\
#                                 .filter(Citizen.counter_id != None)\
#                                 .join(CitizenState)\
#                                 .filter((CitizenState.cs_state_name == 'Active')\
#                                 | (CitizenState.cs_state_name == 'Appointment booked'))\
#                                 .order_by(Citizen.start_time)\
#                                 .all()
# all_appointment =  get_all_booked + get_all_walkin
# get_all_walkin = Citizen.query.filter_by(office_id=citizen.office_id)\
#                                 .filter(Citizen.start_time >= citizen.start_time)\
#                                 .filter(Citizen.start_time <= time_now)\
#                                 .filter(Citizen.counter_id != None)\
#                                 .join(CitizenState)\
#                                 .filter(CitizenState.cs_state_name == 'Active')\
#                                 .order_by(Citizen.start_time.desc())\
#                                 .all()