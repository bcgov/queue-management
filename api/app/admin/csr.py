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

from app.models.theq import Citizen, CSR, CitizenState, Period, PeriodState, ServiceReq, SRState, Counter
from flask import flash, redirect, request
from .base import Base
from flask_admin.babel import gettext
from flask_admin.base import expose
from flask_admin.form import FormOpts
from flask_admin.helpers import get_redirect_target
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_login import current_user
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from qsystem import db, cache, socketio

class CSRConfig(Base):
    roles_allowed = ['GA', 'HELPDESK', 'SUPPORT']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    create_modal = False
    edit_modal = False

    @property
    def can_create(self):
        return current_user.role.role_code != 'GA'

    can_delete = False

    column_list = ['username', 'office.office_name', 'office_manager', 'pesticide_designate', 'finance_designate',
                   'ita2_designate', 'role.role_desc', 'deleted']
    column_labels = {
        'username': 'Username',
        'office.office_name': 'Office',
        'office_manager': 'Office Exam Manager',
        'pesticide_designate': 'Environment Client Liaison/Program Specialist',
        'finance_designate': 'Financial Reporting Designate',
        'ita2_designate': 'ITA Liaison/Program Specialist',
        'role.role_desc': 'Role',
        'deleted': 'Deleted'
    }
    column_searchable_list = ('username',)
    column_sortable_list = ('username', 'office.office_name', 'office_manager', 'pesticide_designate',
                            'finance_designate', 'ita2_designate', 'role.role_desc', 'deleted')
    column_default_sort = 'username'
    form_args = {
        'csr_state': {'default': 'Logout'},
        'office_manager': {'default': '0'},
        'pesticide_designate': {'default': '0'},
        'finance_designate': {'default': '0'},
        'ita2_designate': {'default': '0'},
    }

    #   The defaults if you are SUPPORT
    form_choices = {
        'office_manager': [
            ("0", 'No - not an Exam Manager'), ("1", 'Yes - an Exam Manager')
        ],
        'pesticide_designate': [
            ("0", 'No - not an Environment Specialist'), ("1", 'Yes - an Environment Specialist')
        ],
        'finance_designate': [
            ("0", 'No - not in Finance team'), ("1", 'Yes - for Finance team reporting')
        ],
        'ita2_designate': [
            ("0", 'No - not an ITA Liaison'), ("1", 'Yes - an ITA Liaison')
        ]
    }

    form_excluded_columns = ('periods', 'qt_xn_csr_ind', 'receptionist_ind')
    form_create_rules = ('username', 'office_manager', 'pesticide_designate',
                         'finance_designate', 'ita2_designate', 'csr_state', 'role', 'office','deleted', 'counter')
    form_edit_rules = ('username', 'office_manager', 'pesticide_designate',
                       'finance_designate', 'ita2_designate', 'csr_state', 'role', 'office', 'deleted','counter')

    def get_return_url(self):
        return get_redirect_target() or self.get_url('.index_view')

    def validate_model(self):

        identifier = get_mdict_item_or_list(request.args, 'id')
        if identifier is None:
            return False

        #  Get Invited and Being Served states, to see if CSR has any open tickets.
        period_state_invited = PeriodState.get_state_by_name("Invited")
        period_state_being_served = PeriodState.get_state_by_name("Being Served")

        #  See if CSR has any open tickets.
        citizen = Citizen.query \
            .join(Citizen.service_reqs) \
            .join(ServiceReq.periods) \
            .filter(Period.time_end.is_(None)) \
            .filter(Period.csr_id==identifier) \
            .filter(or_(Period.ps_id==period_state_invited.ps_id, Period.ps_id==period_state_being_served.ps_id)) \
            .all()

        if len(citizen) != 0:
            flash(gettext('CSR has an open ticket and cannot be edited.'), 'error')
            return False

        if not self.can_edit:
            return False

        model = self.get_one(identifier)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return False

        return model

    def handle_view_exception(self, exc):
        if isinstance(exc, IntegrityError):
            flash(gettext('Username already exists in the database.  Duplicate record not created.'))
            return True

    def on_model_change(self, form, model, is_created):

        #  Trim idir name, convert to lower case, regardless of whether edit or create.
        model.username = model.username.strip().lower()

        if is_created:

            if model.receptionist_ind is None:
                model.receptionist_ind = 0

            if model.counter is None:
                counter = Counter.query.filter(Counter.counter_name == 'Counter').first()
                model.counter = counter

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        """
            Edit model view
        """
        return_url = self.get_return_url()
        model = self.validate_model()

        if not model:
            return redirect(return_url)

        csr_id = get_mdict_item_or_list(request.args, 'id')

        form = self.edit_form(obj=model)
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(ruleset=self._form_edit_rules, form=form)

        if self.validate_form(form) and self.update_model(form, model):

            #  Trim the user name, if necessary.
            updated_csr = CSR.query.filter_by(csr_id=csr_id).first()

            check_uservalues(updated_csr)

            socketio.emit('clear_csr_cache', { "id": csr_id})
            socketio.emit('csr_update',
                          {"csr_id": csr_id, "receptionist_ind": updated_csr.receptionist_ind},
                          room=current_user.office.office_name)

            flash(gettext('''Record was successfully saved.'''), 'success')

            request_redirect(self, return_url, model, request)

        if request.method == 'GET' or form.errors:
            self.on_form_prefill(form, id)

        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_edit_rules)

        if self.edit_modal and request.args.get('modal'):
            template = self.edit_modal_template
        else:
            template = self.edit_template

        return self.render(template,
                           model=model,
                           form=form,
                           form_opts=form_opts,
                           return_url=return_url)


class CSRConfigGA(CSRConfig):

    form_excluded_columns = ('periods', 'qt_xn_csr_ind', 'receptionist_ind', 'deleted', 'finance_designate',
                             'csr_state', 'counter')
    form_create_rules = ('username', 'office_manager', 'pesticide_designate',
                         'finance_designate', 'ita2_designate', 'csr_state', 'role', 'office', 'counter')
    form_edit_rules = ('username', 'office_manager', 'pesticide_designate', 'ita2_designate', 'role', 'office')


CSRModelView = CSRConfig(CSR, db.session)
CSRGAModelView = CSRConfigGA(CSR, db.session, endpoint='csrga')


def check_uservalues(updated_csr):

    #  Assume data does not need to be updated
    update_data = False

    #  See if spaces at start or end of user name.
    if updated_csr.username != updated_csr.username.strip():
        updated_csr.username = updated_csr.username.strip()
        update_data = True

    if updated_csr.counter_id is None:
        counter = Counter.query.filter(Counter.counter_name=='Counter').first()
        updated_csr.counter_id = counter.counter_id
        update_data = True

    if update_data:
        db.session.add(updated_csr)
        db.session.commit()


def request_redirect(self, return_url, model, request_parameter):

    if '_add_another' in request_parameter.form:
        return redirect(self.get_url('.create_view', url=return_url))
    elif '_continue_editing' in request.form:
        return redirect(request_parameter.url)
    else:
        return redirect(self.get_save_return_url(model, is_created=False))
