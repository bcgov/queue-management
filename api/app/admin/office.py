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



from app.models.theq import Office, Service, Counter
from .base import Base
from flask_login import current_user
from flask import flash, url_for
from flask_admin.babel import gettext
from qsystem import db
from sqlalchemy import and_
from qsystem import db, cache, socketio
from pprint import pprint
from wtforms import TextAreaField
from app.models.theq import CSR


def on_form_prefill(counters):
    print('==>on_form_prefill ===> office.py Flask Admin ===> counters',counters)


class OfficeConfig(Base):
    roles_allowed = ['SUPPORT', 'GA']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    @property
    def can_create(self):
        return current_user.role.role_code != 'GA'

    def get_query(self):
        if current_user.role.role_code == 'SUPPORT':
            return self.session.query(self.model)
        elif current_user.role.role_code == 'GA':
            return self.session.query(self.model).filter_by(office_id=current_user.office_id)

    create_modal = False
    edit_modal = False
    can_delete = False
    form_create_rules = ('office_name', 'office_number', 'sb', 'services', 'deleted', 'exams_enabled_ind',
                         'appointments_enabled_ind', 'timezone', 'latitude', 'longitude', 'office_appointment_message',
                         'appointments_days_limit', 'appointment_duration', 'soonest_appointment', 'max_person_appointment_per_day',\
                         'civic_address', 'telephone', 'online_status', 'check_in_notification', 'check_in_reminder_msg',\
                         'automatic_reminder_at', 'currently_waiting', 'digital_signage_message', 'digital_signage_message_1',\
                         'digital_signage_message_2', 'digital_signage_message_3', 'show_currently_waiting_bottom' )
    form_edit_rules = ('office_name', 'office_number', 'sb', 'services', 'deleted', 'exams_enabled_ind',
                       'appointments_enabled_ind', 'timezone', 'latitude', 'longitude', 'office_appointment_message',
                         'appointments_days_limit', 'appointment_duration', 'soonest_appointment', 'max_person_appointment_per_day',\
                         'civic_address', 'telephone', 'online_status', 'check_in_notification', 'check_in_reminder_msg', \
                         'automatic_reminder_at', 'currently_waiting', 'digital_signage_message', 'digital_signage_message_1',\
                         'digital_signage_message_2', 'digital_signage_message_3', 'show_currently_waiting_bottom' )
    form_choices = {
        'exams_enabled_ind': [
            ("0", 'No - Exams are not enabled for this office'), \
            ("1", 'Yes - Exams are enabled for this office')
        ],
        'appointments_enabled_ind': [
            ("0", 'No - Appointments are not enabled for this office'), \
            ("1", 'Yes - Appointments are enabled for this office')
        ],
        'check_in_notification': [
            ("0", 'Off - Disabale Notifications'), \
            ("1", 'On - Enable Notifications')
        ],
        'automatic_reminder_at': [
            ("0", 'Off - Disable Feature'), \
            ("1", '1 - First in Line'), \
            ("2", '2 - Second in Line'),\
            ("3", '3 - Third in Line')
        ],
        'currently_waiting': [
            ("0", 'Off - Disabale Currently Waiting in SmartBoard'), \
            ("1", 'On - Enable Currently Waiting in SmartBoard')
        ],
        'digital_signage_message': [
            ("0", 'Off - Disabale Messages in SmartBoard'), \
            ("1", 'On - Enable Messages in SmartBoard')
        ],
        'show_currently_waiting_bottom': [
            ("0", 'Off - Hide Currently Waiting at bottom in SmartBoard'), \
            ("1", 'On - Show Currently Waiting  from bottom in SmartBoard')
        ],
    }
    column_labels = {'sb': 'Smartboard', 'timezone.timezone_name': 'Timezone Name'}
    column_searchable_list = ('office_name',)
    column_sortable_list = ['office_name', 'sb', 'deleted', 'exams_enabled_ind']
    column_list = ['office_name',
                   'sb',
                   'services',
                   'deleted',
                   'exams_enabled_ind',
                   'appointments_enabled_ind',
                   'counters',
                   'timezone.timezone_name',
                   'latitude',
                   'longitude',
                   'office_appointment_message',
                   'appointments_days_limit',
                   'appointment_duration',
                   'max_person_appointment_per_day',
                   'civic_address',
                   'timeslots',
                   'number_of_dlkt',
                   'office_email_paragraph',
                   'external_map_link',
                   'check_in_notification',
                   'check_in_reminder_msg',
                   'automatic_reminder_at',
                    'currently_waiting',
                    'digital_signage_message',
                    'digital_signage_message_1',
                    'digital_signage_message_2',
                    'digital_signage_message_3',
                    'show_currently_waiting_bottom',
                   ]

    form_excluded_columns = ('citizens',
                             'csrs',
                             'exams',
                             'rooms',
                             'invigilators'
                             )

    form_create_rules = ('office_name',
                        'office_number',                       
                        'services',                       
                        'exams_enabled_ind',                       
                        'counters',
                        'quick_list',
                        'back_office_list',
                        'timezone',
                        'sb',  
                        'currently_waiting',
                        'show_currently_waiting_bottom',
                        'digital_signage_message',
                        'digital_signage_message_1',
                        'digital_signage_message_2',
                        'digital_signage_message_3',    
                        'check_in_notification',
                        'check_in_reminder_msg',
                        'automatic_reminder_at',  
                        'appointments_enabled_ind',
                        'appointment_duration',
                        'office_email_paragraph',
                        'online_status',
                        'office_appointment_message',
                        'latitude',
                        'longitude',
                        'civic_address',
                        'telephone',
                        'external_map_link',
                        'appointments_days_limit',
                        'soonest_appointment',
                        'max_person_appointment_per_day',                                                                     
                        'number_of_dlkt',
                        'timeslots',
                        'deleted',
                        )

    form_edit_rules = ('office_name',
                       'office_number',                       
                       'services',                       
                       'exams_enabled_ind',                       
                       'counters',
                       'quick_list',
                       'back_office_list',
                       'timezone',
                       'sb',  
                       'currently_waiting',
                       'show_currently_waiting_bottom',
                       'digital_signage_message',
                       'digital_signage_message_1',
                       'digital_signage_message_2',
                       'digital_signage_message_3',    
                       'check_in_notification',
                       'check_in_reminder_msg',
                       'automatic_reminder_at',  
                       'appointments_enabled_ind',
                       'appointment_duration',
                       'office_email_paragraph',
                       'online_status',
                       'office_appointment_message',
                       'latitude',
                       'longitude',
                       'civic_address',
                       'telephone',
                       'external_map_link',
                       'appointments_days_limit',
                       'soonest_appointment',
                       'max_person_appointment_per_day',                                                                     
                       'number_of_dlkt',
                       'timeslots',
                       'deleted',
                       )

    form_args = {
        'quick_list': {
            'query_factory': lambda: db.session.query(Service) \
                                               .filter(and_(Service.parent_id.isnot(None)), \
                                                       and_(Service.deleted.is_(None)), \
                                                            Service.display_dashboard_ind == 1)
        },
        'back_office_list': {
            'query_factory': lambda: db.session.query(Service) \
                                               .filter(and_(Service.parent_id.isnot(None)), \
                                                       and_(Service.deleted.is_(None)), \
                                                            Service.display_dashboard_ind == 0)
        },
        'appointments_days_limit': {'default': '30'},
        'appointment_duration': {'default': '30'},
        'max_person_appointment_per_day': {'default': '1'}

    }

    column_labels = {'sb': 'Smartboard',
                     'timezone.timezone_name': 'Timezone Name',
                     'exams_enabled_ind': 'Exams Enabled',
                     'appointments_enabled_ind': 'Appointments Enabled',
                     'office_appointment_message': 'Online Appointment Message',
                     'appointments_days_limit': 'Appointment Days Limit',
                     'max_person_appointment_per_day': 'Maximum number of appointments allowed for same person per day',
                     'office_email_paragraph': 'Office Email Paragraph',
                     'soonest_appointment': 'Soonest Appointment (minutes)',
                     'appointment_duration': 'Default Appointment Duration',
                     'check_in_notification': 'Check-In Notifications',
                     'check_in_reminder_msg': 'Check-In Notification Reminder Message',
                     'automatic_reminder_at': 'Check-In Notification Automatically Send Message When Ticket is X in Line',
                     'currently_waiting': 'Display Citizen Details on Smartboard',
                     'digital_signage_message': 'Digital Signage Message in SmartBoard',
                     'digital_signage_message_1': 'Digital Signage Message 1',
                     'digital_signage_message_2': 'Digital Signage Message 2',
                     'digital_signage_message_3': 'Digital Signage Message 3',
                     'show_currently_waiting_bottom': 'Show Currently Waiting at Bottom in SmartBoard'
                     }

    column_sortable_list = ['office_name',
                            'sb',
                            'deleted',
                            'exams_enabled_ind',
                            'exams_enabled_ind',
                            'appointments_enabled_ind',
                             'counters',
                            'quick_list',
                            'back_office_list',
                            ]

    column_default_sort = 'office_name'

    form_widget_args = {
        'office_email_paragraph': { 'rows': 5, 'maxlength': 2000  }
    }

    form_overrides = {
        'office_email_paragraph': TextAreaField
    }

    #     if is_created:
    #         print('==>init_formdata  ===> is_created True')
    #     #     print('==>on_model_change  ===> Office.counters', Office.counters)
    #     print('==>init_formdata  ===> Office.counters.counter_id', Office.counters.counter_id)
    #     #     print('==>on_model_change  ===> Counter.counter_id:', Counter.counter_id)
    #     #     print('==>on_model_change  ===> Counter.counter_name:', Counter.counter_name)
    #     #     print('==>on_model_change  ===> model.counters:', model.counters)
    #     counter = Office.query.filter(Office.counters.counter_id == 2).first()
    #     print('==>on_model_change  ===> init_formdata:', counter)
    #     form.Office.process_formdata(counter)
    #     #     if model.counters is None:
    #     #
    #     #
    #     #         model.counters = counter
    #     #         print('==>on_model_change  ===> model.counter:',model.counter)

    # def on_model_change(self, form, model, is_created):
    #     print('==>on_model_change  ===> office.py Flask Admin')
    #     """Invoked on model change."""
    #     socketio.emit('update_offices_cache')
    #
    #     invalid = []
    #     for service in model.quick_list:
    #         if service not in model.services:
    #             invalid.append(str(service))
    #             model.quick_list.remove(service)
    #     if len(invalid) != 0:
    #         message = ", ".join(invalid)
    #         flash(gettext("Services saved minus services not offered at this office: " + message), 'warning')
    #
    #     print("==> on_model_change for Office")
    #     print("    --> Counter.counter_name")
    #     pprint(Counter.counter_name)
    #     # print("    --> Counter.counter_name")
    #     # pprint(Counter.counter_name)
    #     # print("    --> model.counters")
    #     # pprint(model.counters)
    #     counterItem = Counter.query.filter(Counter.counter_id == 2).first()
    #     print("    --> counterItem.counter_name")
    #     pprint(counterItem.counter_id)
    #     pprint(counterItem.counter_name)
    #     Office.counters.model.counters.counter_id = counterItem.counter_id
    #     model.counters.counter_name = counterItem.counter_name
    #     print("    --> model.counters  last line, what is value")
    #     pprint(model.counters.counter_id)
    #     pprint(model.counters.counter_name)
    
    def on_model_change(self, form, model, is_created):
        csr = CSR.find_by_username(current_user.username)
        socketio.emit('clear_csr_cache', { "id": csr.csr_id})
        socketio.emit('csr_update',
                        {"csr_id": csr.csr_id, "receptionist_ind": csr.receptionist_ind},
                        room=csr.office.office_name)
        socketio.emit('digital_signage_msg_update')

    def render(self, template, **kwargs):
        if current_user.role.role_code == 'SUPPORT':
            self.extra_js = [url_for("static", filename="js/office.js")]
        elif current_user.role.role_code == 'GA':
            self.extra_js = [url_for("static", filename="js/officega.js")]
        return super(OfficeConfig, self).render(template, **kwargs)            

class OfficeConfigGA(OfficeConfig):

    #  Change what GA sees on the Office List view.
    column_labels = {
        'quick_list': 'Quick List',
        'back_office_list': 'Back Office List',
        'currently_waiting': 'Display Citizen Details on Smartboard',
        'show_currently_waiting_bottom': 'Show Currently Waiting at Bottom in SmartBoard',
        'check_in_reminder_msg': 'Check-In Notification Reminder Message',
        'automatic_reminder_at': 'Check-In Notification Automatically Send Message When Ticket is X in Line',
        'soonest_appointment': 'Soonest Appointment (minutes)',
        'appointment_duration': 'Default Appointment Duration'
    }

    column_list = [
        'office_name',
        'quick_list',
        'back_office_list'
    ]

    #  Change what GAs are allowed to do from what SUPPORT can do.
    form_edit_rules = (
        'office_name',
        'counters',
        'quick_list',
        'back_office_list',
        'sb',
        'currently_waiting',
        'show_currently_waiting_bottom',
        'digital_signage_message',
        'digital_signage_message_1',
        'digital_signage_message_2',
        'digital_signage_message_3',
        'check_in_notification',
        'check_in_reminder_msg',
        'automatic_reminder_at',
        'appointments_enabled_ind',
        'appointment_duration',
        'office_email_paragraph',
        'online_status',
        'office_appointment_message',        
        'civic_address',
        'telephone',
        'external_map_link',
        'appointments_days_limit',        
        'soonest_appointment',
        'max_person_appointment_per_day',
        'number_of_dlkt',        
    )

    form_excluded_columns = (
        'office_number',
        'services',
        'exams_enabled_ind',        
        'latitude',
        'longitude',
        'timeslots',
        'deleted',
        'timezone',
        'citizens',
        'csrs',
        'exams',
        'rooms',
        'invigilators',
    )

    form_widget_args = {
        'office_name': {
            'readonly': True
        },
        'appointments_enabled_ind': {
            'readonly': True
        },
        'online_status': {
            'readyonly': True
        },
        'office_email_paragraph': { 'rows': 5, 'maxlength': 2000  }
    }

OfficeModelView = OfficeConfig(Office, db.session)
OfficeGAModelView = OfficeConfigGA(Office, db.session, endpoint='officega')
