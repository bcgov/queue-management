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
from qsystem import api, api_call_with_retry, db, socketio, my_print, application
from app.models.theq import Citizen, CSR, Counter, Office, CitizenState, ServiceReq
from app.models.bookings import Appointment
from marshmallow import ValidationError
from app.schemas.theq import CitizenSchema, OfficeSchema
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
    office_schema = OfficeSchema()

    def get(self, id):
        try:
            citizen = Citizen.query.filter_by(walkin_unique_id=id).join(CitizenState)\
                                            .filter(CitizenState.cs_state_name == 'Active')\
                                            .order_by(Citizen.citizen_id.desc()).first()
            if citizen:
                booked_not_checkin = []
                serving_app = []
                booked_check_app = []
                walkin_app = []
                res_list = []
                my_office = Office.query.filter_by(office_id=citizen.office_id).first()
                my_office_data = self.office_schema.dump(my_office)
                local_timezone = False 
                if my_office_data:
                    my_time_zone = my_office_data['timezone']['timezone_name']
                    local_timezone = pytz.timezone(my_time_zone)
                my_result = self.citizen_schema.dump(citizen)
                am_on_hold = False
                citizen_service_reqs = my_result.get('service_reqs', [])
                for j in citizen_service_reqs:
                    my_served_period = sorted(j['periods'], key= lambda x:x['period_id'], reverse=True)[0]
                    if my_served_period:
                        if (my_served_period['ps']['ps_name'] == 'On hold'):
                            am_on_hold = True
                show_estimate = application.config.get('SHOW_ESTIMATE_TIME_WALKIN', False)
                time_now = datetime.utcnow()
                past_hour = datetime.utcnow() - timedelta(hours=1)
                future_hour = datetime.utcnow() + timedelta(hours=4)
                
                all_citizen_in_q = Citizen.query.filter_by(office_id=citizen.office_id) \
                                                .join(CitizenState)\
                                                .filter(CitizenState.cs_state_name == 'Active')\
                                                .order_by(Citizen.priority) \
                                                .join(Citizen.service_reqs).all()
                result = self.citizens_schema.dump(all_citizen_in_q)
                local_past = pytz.utc.localize(past_hour)
                local_future = pytz.utc.localize(future_hour)
                # getting agenda panel app
                appointments = Appointment.query.filter_by(office_id=citizen.office_id)\
                                            .filter(Appointment.start_time <= local_future)\
                                            .filter(Appointment.start_time >= local_past)\
                                            .filter(Appointment.checked_in_time == None)\
                                            .order_by(Appointment.start_time)\
                                            .all()
                result_in_Book = self.appointment_schema.dump(appointments)
                # processing agenda panel appointmnets:
                # .filter(Appointment.is_draft != False)\
                # .filter(Appointment.blackout_flag != 'Y')\
                for app in result_in_Book:
                    if not (app.get('is_draft', True)) and (app.get('blackout_flag', 'N') == 'N')  and not (app.get('stat_flag', True)):
                        data_dict = {}
                        data_dict['flag'] = 'agenda_panel'
                        data_dict['start_time'] = app.get('start_time',  '')
                        if data_dict['start_time'] and local_timezone:
                            utc_datetime = datetime.strptime(data_dict['start_time'], '%Y-%m-%dT%H:%M:%S%z')
                            local_datetime = utc_datetime.replace(tzinfo=pytz.utc)
                            local_datetime = local_datetime.astimezone(local_timezone)
                            data_dict['start_time'] = local_datetime.strftime("%m/%d/%Y, %H:%M:%S")
                        booked_not_checkin.append(data_dict)
                for each in result:
                    data_dict = {}
                    if bool(each.get('service_reqs', False)):
                        for i in each['service_reqs']:
                            served_period = sorted(i['periods'], key= lambda x:x['period_id'], reverse=True)[0]
                            if served_period:
                                if served_period['ps']['ps_name'] == 'Being Served':
                                    data_dict['flag'] = 'serving_app'
                                    data_dict['ticket_number'] = each.get('ticket_number', '')
                                    data_dict['walkin_unique_id'] = each.get('walkin_unique_id', '')
                                    data_dict['service_begin_seconds'] = (datetime.utcnow()-datetime.strptime(served_period['time_start'], '%Y-%m-%dT%H:%M:%S.%f')).total_seconds()
                                    serving_app.append(data_dict)
                                    data_dict = {}
                                    break
                                if (not (served_period['time_end']) and (served_period['ps']['ps_name'] in ('Waiting', 'Invited'))):
                                    not_booked_flag = False
                                    data_dict = {}
                                    data_dict['ticket_number'] = each.get('ticket_number', '')
                                    data_dict['walkin_unique_id'] = each.get('walkin_unique_id', '') 
                                    if (each.get('citizen_comments', '')):
                                        if '|||' in each['citizen_comments']:
                                            data_dict['flag'] = 'booked_app'
                                            booked_check_app.append(data_dict)
                                            data_dict = {}
                                            break
                                        else:
                                            not_booked_flag = True
                                    else:
                                        not_booked_flag = True
                                    if not_booked_flag and each.get('cs', False):
                                        if each['cs'].get('cs_state_name', '') == 'Active':
                                            each_time_obj = datetime.strptime(each['start_time'], '%Y-%m-%dT%H:%M:%SZ')
                                            if am_on_hold:
                                                data_dict['flag'] = 'walkin_app'
                                                walkin_app.append(data_dict)
                                                data_dict = {}
                                                break
                                            else:
                                                if each_time_obj <= citizen.start_time:
                                                    data_dict['flag'] = 'walkin_app'
                                                    walkin_app.append(data_dict)
                                                    data_dict = {}
                                                    break
                res_list = tuple(serving_app+booked_check_app+booked_not_checkin+walkin_app)
                return {'citizen': res_list, 'show_estimate': show_estimate}, 200
            return {}
        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500

            
                                            # .filter((Appointment.checked_in_time )\
                                            #  (Appointment.is_draft != False)\
                                            # | (Appointment.blackout_flag != 'Y'))\