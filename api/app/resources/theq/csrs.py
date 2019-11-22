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

from datetime import datetime
from flask import g
from flask_restplus import Resource
from qsystem import api, db, oidc, application, api_call_with_retry
from sqlalchemy import exc, or_
from app.models.bookings import Exam, ExamType, Booking
from app.models.theq import Citizen, CSR, Period, ServiceReq, SRState
from app.schemas.bookings import ExamSchema, ExamTypeSchema
from app.schemas.theq import CitizenSchema, CSRSchema
import pytz

@api.route("/csrs/", methods=["GET"])
class CsrList(Resource):

    csr_schema = CSRSchema(many=True, exclude=('office', 'periods',))

    @oidc.accept_token(require_token=True)
    def get(self):
        try:
            csr = CSR.find_by_username(g.oidc_token_info['username'])

            if csr.role.role_code != "GA":
                return {'message': 'You do not have permission to view this end-point'}, 403

            csrs = CSR.query.filter_by(office_id=csr.office_id)
            filtered_csrs = [c for c in csrs if c.deleted is None]
            result = self.csr_schema.dump(filtered_csrs)

            return {'csrs': result.data,
                    'errors': result.errors}

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500


@api.route("/csrs/me/", methods=["GET"])
class CsrSelf(Resource):

    csr_schema = CSRSchema()
    citizen_schema = CitizenSchema(many=True)
    exam_schema = ExamSchema(many=True)
    exam_type_schema = ExamTypeSchema()
    timezone = pytz.timezone("US/Pacific")
    back_office_display = application.config['BACK_OFFICE_DISPLAY']
    recurring_feature_flag = application.config['RECURRING_FEATURE_FLAG']

    @oidc.accept_token(require_token=True)
    @api_call_with_retry
    def get(self):
        try:
            csr = CSR.find_by_username(g.oidc_token_info['username'])

            if not csr:
                return {'Message': 'User Not Found'}, 404

            db.session.add(csr)
            active_sr_state = SRState.get_state_by_name("Active")
            today = datetime.now()
            start_date = self.timezone.localize(today)

            active_citizens = Citizen.query \
                .join(Citizen.service_reqs) \
                .filter_by(sr_state_id=active_sr_state.sr_state_id) \
                .join(ServiceReq.periods) \
                .filter_by(csr_id=csr.csr_id) \
                .filter(Period.time_end.is_(None))

            #   Get a list of all current exams for the office.
            office_exams = Exam.query \
                .filter(Exam.office_id == csr.office_id, \
                        Exam.exam_returned_date.is_(None), \
                        Exam.deleted_date.is_(None)) \
                .join(ExamType, Exam.exam_type_id == ExamType.exam_type_id) \
                .outerjoin(Booking, Exam.booking_id == Booking.booking_id) \
                .outerjoin(Booking.booking_invigilators, Booking.booking_id == Booking.booking_invigilators.c.invigilator_id)

            #   Default condition ... attention is not needed for any exam.
            attention_needed = False

            #   Check for attention needed, individual exam.
            individual = []
            for exam in office_exams:
                if exam.exam_type.group_exam_ind == 0 and exam.exam_type.exam_type_name != 'Monthly Session Exam':
                    attention_needed = attention_needed or exam.expiry_date <= start_date
                    if exam.booking is not None:
                        if exam.booking.end_time < start_date:
                            attention_needed = True
                    if attention_needed:
                        individual.append(exam)

            #   Check for attention needed, monthly session exam, only if attention not already needed.

            # if not attention_needed:
            #   TAKE OUT!!!!!
            attention_needed = False
            monthly = []
            if not attention_needed:
                for exam in office_exams:
                    if exam.exam_type.exam_type_name == 'Monthly Session Exam':
                        if exam.booking is None:
                            attention_needed = True
                        else:
                            attention_needed = attention_needed or len(exam.booking.invigilators) == 0
                            attention_needed = attention_needed or exam.booking.end_time < start_date
                        if attention_needed:
                            monthly.append(exam)

            # if not attention_needed:
            #   TAKE OUT!!!!!
            attention_needed = False
            group = []
            if not attention_needed:
                for exam in office_exams:
                    if exam.exam_type.group_exam_ind == 1:
                        if exam.booking is None:
                            attention_needed = True
                        else:
                            attention_needed = attention_needed or len(exam.booking.invigilators) == 0
                            attention_needed = attention_needed or exam.booking.end_time < start_date
                        if attention_needed:
                            group.append(exam)

            result = self.csr_schema.dump(csr)
            active_citizens = self.citizen_schema.dump(active_citizens)

            return {'csr': result.data,
                    'attention_needed': attention_needed,
                    'active_citizens': active_citizens.data,
                    'back_office_display': self.back_office_display,
                    'recurring_feature_flag': self.recurring_feature_flag,
                    'errors': result.errors}

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500
