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
from app.utilities.email import send_email, get_walkin_reminder_email_contents
from app.utilities.sms import send_walkin_reminder_sms
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import raiseload, joinedload

# Defining String constants to appease SonarQube
api_down_const = 'API is down'

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
                res_list = []
                # office time zone
                local_timezone = self.get_my_office_timezone(citizen = citizen)

                # am i on hold
                am_on_hold = self.am_i_on_hold(citizen)

                show_estimate = application.config.get('SHOW_ESTIMATE_TIME_WALKIN', False)
                
                # result= all citizen in q
                result = self.get_all_citizen_in_q(citizen = citizen)
                # process result
                booked_check_app, walkin_app = self.process_all_citizen_in_q(result, citizen, am_on_hold, local_timezone)

                # get all app from agenda panel
                result_in_book = self.get_all_app_from_agenda_panel(citizen=citizen)
                # processing agenda panel appointmnets:
                booked_not_checkin = self.process_agenda_panel(result_in_book, local_timezone)
                
                # sorting-maintaing the order group 
                # serving people dont want see
                res_list = tuple(booked_check_app + booked_not_checkin + walkin_app)

                return {'citizen': res_list, 'show_estimate': show_estimate}, 200
            return {}
        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': api_down_const}, 500

    def get_my_office_timezone(self, citizen=False, office=False):
        office_id = False
        local_timezone = False 
        if citizen:
            office_id = citizen.office_id
        if office:
            office_id = office.office_id
        if office_id:
            my_office = Office.query.filter_by(office_id=office_id).first()
            my_office_data = self.office_schema.dump(my_office)
            if my_office_data:
                my_time_zone = my_office_data['timezone']['timezone_name']
                local_timezone = pytz.timezone(my_time_zone)
        return local_timezone
    
    def am_i_on_hold(self, citizen):
        my_result = self.citizen_schema.dump(citizen)
        am_on_hold = False
        citizen_service_reqs = my_result.get('service_reqs', [])
        for j in citizen_service_reqs:
            my_served_period = sorted(j['periods'], key= lambda x:x['period_id'], reverse=True)[0]
            if my_served_period and (my_served_period['ps']['ps_name'] == 'On hold'):
                am_on_hold = True
        return am_on_hold
    
    def get_all_citizen_in_q(self, citizen=False, office=False):
        office_id = False
        result = []
        if citizen:
            office_id = citizen.office_id
        if office:
            office_id = office.office_id
        if office_id:  
            all_citizen_in_q = Citizen.query.filter_by(office_id=office_id) \
                                            .join(CitizenState)\
                                            .filter(CitizenState.cs_state_name == 'Active')\
                                            .order_by(Citizen.priority) \
                                            .join(Citizen.service_reqs).all()
            result = self.citizens_schema.dump(all_citizen_in_q)
        return result

    def process_all_citizen_in_q(self, result, citizen, am_on_hold, local_timezone):
        booked_check_app = []
        walkin_app = []
        for each in result:
            data_dict = {}
            if bool(each.get('service_reqs', False)):
                for i in each['service_reqs']:
                    served_period = sorted(i['periods'], key= lambda x:x['period_id'], reverse=True)[0]
                    if served_period and (not (served_period['time_end']) and (served_period['ps']['ps_name'] in ('Waiting', 'Invited'))):
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
                        if (not_booked_flag and each.get('cs', False)) and each['cs'].get('cs_state_name', '') == 'Active':
                            each_time_obj = datetime.strptime(each['start_time'], '%Y-%m-%dT%H:%M:%SZ')
                            # start
                            local_datetime_start = each_time_obj.replace(tzinfo=pytz.utc).astimezone(local_timezone)
                            #end
                            local_datetime_end = citizen.start_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)                                    
                            if am_on_hold or local_datetime_start <= local_datetime_end:
                                data_dict['flag'] = 'walkin_app'
                                walkin_app.append(data_dict)
                                data_dict = {}
                                break
        return booked_check_app, walkin_app
    
    def get_all_app_from_agenda_panel(self,  citizen=False, office=False):
        office_id = False
        result_in_book = []
        if citizen:
            office_id = citizen.office_id
        if office:
            office_id = office.office_id
        if office_id:  
            past_hour = datetime.utcnow() - timedelta(minutes=15)
            future_hour = datetime.utcnow() + timedelta(minutes=15)
            local_past = pytz.utc.localize(past_hour)
            local_future = pytz.utc.localize(future_hour)
            # getting agenda panel app
            appointments = Appointment.query.filter_by(office_id=office_id)\
                                        .filter(Appointment.start_time <= local_future)\
                                        .filter(Appointment.start_time >= local_past)\
                                        .filter(Appointment.checked_in_time == None)\
                                        .order_by(Appointment.start_time)\
                                        .all()
            result_in_book = self.appointment_schema.dump(appointments)
        return result_in_book

    def process_agenda_panel(self, result_in_book, local_timezone):
        booked_not_checkin = []
        for app in result_in_book:
            if not (app.get('is_draft', True)) and (app.get('blackout_flag', 'N') == 'N')  and not (app.get('stat_flag', True)):
                data_dict = {}
                data_dict['flag'] = 'agenda_panel'
                data_dict['start_time'] = app.get('start_time',  '')
                if data_dict['start_time'] and local_timezone:
                    if (len(data_dict['start_time']) >= 3) and ':' in data_dict['start_time'][-3]:
                        data_dict['start_time'] = '{}{}'.format(data_dict['start_time'][:-3], data_dict['start_time'][-2:])
                    utc_datetime = datetime.strptime(data_dict['start_time'], '%Y-%m-%dT%H:%M:%S%z')
                    local_datetime = utc_datetime.replace(tzinfo=pytz.utc)
                    local_datetime = local_datetime.astimezone(local_timezone)
                    data_dict['start_time'] = local_datetime.strftime("%m/%d/%Y, %H:%M:%S")
                booked_not_checkin.append(data_dict)
        return booked_not_checkin

@api.route("/send-reminder/line-walkin/", methods=["POST"])
class SendLineReminderWalkin(Resource):
    citizen_schema = CitizenSchema()
    office_schema = OfficeSchema()
    walkinObj = WalkinDetail()

    @jwt.has_one_of_roles([Role.internal_user.value])
    @api_call_with_retry
    def post(self):
        try:
            result = []
            json_data = request.get_json()
            previous_citizen_id = json_data.get('previous_citizen_id', False)
            if previous_citizen_id:
                previous_citizen = Citizen.query.filter_by(citizen_id=previous_citizen_id).first()
                # get nth line
                nth_line = self.get_nth_line(previous_citizen)

                # get all in Q + Agenda panel
                res_list = []
                
                # result= all citizen in q
                result = self.walkinObj.get_all_citizen_in_q(citizen = previous_citizen)
                # process result
                # am_on_true= means get all citizen in Q
                booked_check_app, walkin_app = self.process_all_citizen_in_q(result)
                
                # sorting-maintaing the order group 
                res_list = tuple(booked_check_app + walkin_app)
                # get the nth object in checkedin and walkin list
                # bool checks for both False and 0
                nth_app = False
                if nth_line and len(res_list) >= int(nth_line) and (int(nth_line) > 0):
                    # Check first n citizens in line
                    for cit in res_list[:int(nth_line)]:
                        nth_app = cit
                        if nth_app['citizen_id']:
                            citizen = Citizen.query \
                            .options(raiseload(Citizen.service_reqs),raiseload(Citizen.office),raiseload(Citizen.user),raiseload(Citizen.cs),raiseload(Citizen.counter)) \
                            .filter_by(citizen_id=nth_app['citizen_id']) \
                            .first()
                            if (not (citizen.automatic_reminder_flag) or (citizen.automatic_reminder_flag == 0)) and citizen.start_position and citizen.start_position >=int(nth_line):
                                office_obj = Office.find_by_id(citizen.office_id)
                                if citizen.notification_phone:
                                    citizen = self.send_sms_reminder(citizen, office_obj)
                                    citizen.automatic_reminder_flag = 1
                                if citizen.notification_email:
                                    citizen = self.send_email_reminder(citizen, office_obj)
                                    citizen.automatic_reminder_flag = 1
                                if citizen.automatic_reminder_flag == 1:
                                    db.session.add(citizen)
                                    db.session.commit()
                result = self.citizen_schema.dump(previous_citizen)
            return {'citizen': result,
                    'errors': self.citizen_schema.validate(previous_citizen)}, 200
        except ValidationError as err:
            return {'message': err.messages}, 422

    def get_nth_line(self, citizen):
        my_office = Office.query.filter_by(office_id=citizen.office_id).first()
        my_office_data = self.office_schema.dump(my_office)
        nth_line = False
        if my_office_data:
            nth_line = my_office_data.get('automatic_reminder_at', False)
        return nth_line

    def process_all_citizen_in_q(self, result):
        booked_check_app = []
        walkin_app = []
        for each in result:
            data_dict = {}
            if bool(each.get('service_reqs', False)):
                for i in each['service_reqs']:
                    served_period = sorted(i['periods'], key= lambda x:x['period_id'], reverse=True)[0]
                    if served_period and (not (served_period['time_end']) and (served_period['ps']['ps_name'] in ('Waiting', 'Invited'))):
                        not_booked_flag = False
                        data_dict = {}
                        data_dict['citizen_id'] = each.get('citizen_id', False)
                        data_dict['service_name'] = i['service']['parent']['service_name']
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
                        if not_booked_flag and each.get('cs', False) and each['cs'].get('cs_state_name', '') == 'Active':
                            data_dict['flag'] = 'walkin_app'
                            data_dict['created_at'] = each.get('created_at', '')
                            walkin_app.append(data_dict)
                            data_dict = {}
                            break
        return booked_check_app, walkin_app

    def send_sms_reminder(self, citizen, office_obj):
        if (citizen.notification_phone):
            sms_sent = False
            validate_check = True
            # code/function call to send sms notification,
            if citizen.reminder_flag and (citizen.reminder_flag == 2):
                validate_check =  False
            if validate_check:
                sms_sent = send_walkin_reminder_sms(citizen, office_obj, request.headers['Authorization'].replace('Bearer ', ''))
                if (sms_sent):
                    flag_value = 1
                    if citizen.reminder_flag == 1:
                        flag_value = 2
                    citizen.reminder_flag = flag_value
                    citizen.notification_sent_time = datetime.utcnow()
        return citizen
                
    
    def send_email_reminder(self, citizen, office_obj):
        if (citizen.notification_email):
            # code/function call to send first email notification,
            email_sent = False
            validate_check = True
            if citizen.reminder_flag and (citizen.reminder_flag == 2):
                validate_check =  False
            if validate_check:
                email_sent = get_walkin_reminder_email_contents(citizen, office_obj)
                if email_sent:
                    send_email(request.headers['Authorization'].replace('Bearer ', ''), *email_sent)
                    flag_value = 1
                    if citizen.reminder_flag == 1:
                        flag_value = 2
                    citizen.reminder_flag = flag_value
                    citizen.notification_sent_time = datetime.utcnow()
        return citizen

@api.route("/smardboard/Q-details/waiting/<string:id>", methods=["GET"])
class SmartBoradQDetails(Resource):
    citizen_schema = CitizenSchema()
    office_schema = OfficeSchema()
    walkinObj = WalkinDetail()
    processObj = SendLineReminderWalkin()

    @api_call_with_retry
    def get(self, id):
        try:
            # get office details from url id
            office = Office.query.filter_by(office_number=id).first()

            if not office:
                return {'message': 'office_number could not be found.'}, 400

            res_list = []
            if (office.currently_waiting == 1):                
                # result= all citizen in q
                result = self.walkinObj.get_all_citizen_in_q(office = office)
                # process result
                booked_check_app, walkin_app = self.processObj.process_all_citizen_in_q(result)
                
                # sorting-maintaing the order group 
                res_list = tuple(booked_check_app + walkin_app)

            return {'citizen_in_q': res_list}, 200
            return {}
        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': api_down_const}, 500

@api.route("/smardboard/Q-details/upcoming/<string:id>", methods=["GET"])
class SmartBoradQDetails(Resource):
    citizen_schema = CitizenSchema()
    office_schema = OfficeSchema()
    walkinObj = WalkinDetail()
    processObj = SendLineReminderWalkin()

    @api_call_with_retry
    def get(self, id):
        try:
            # get office details from url id
            office = Office.query.filter_by(office_number=id).first()

            if not office:
                return {'message': 'office_number could not be found.'}, 400

            booked_not_checkin = []
            if (office.currently_waiting == 1):
                # office time zone
                local_timezone = self.walkinObj.get_my_office_timezone(office = office)

                # get all app from agenda panel
                result_in_book = self.walkinObj.get_all_app_from_agenda_panel(office = office)
                # processing agenda panel appointmnets:
                booked_not_checkin = self.walkinObj.process_agenda_panel(result_in_book, local_timezone)
                
            return {'booked_not_checkin': booked_not_checkin}, 200
            return {}
        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': api_down_const}, 500