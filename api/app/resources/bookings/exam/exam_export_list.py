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
from flask import g, request, make_response
from flask_restplus import Resource
from sqlalchemy import exc
from app.models.bookings import Exam, Booking, Invigilator, Room, ExamType
from app.models.theq import CSR, Office
from app.schemas.bookings import ExamSchema
from qsystem import api, oidc
from datetime import datetime, timedelta
import pytz
import csv
import io


@api.route("/exams/export/", methods=["GET"])
class ExamList(Resource):

    exam_schema = ExamSchema(many=True)

    timezone = pytz.timezone("US/Pacific")

    @oidc.accept_token(require_token=True)
    def get(self):
        try:
            csr = CSR.find_by_username(g.oidc_token_info['username'])

            start_param = request.args.get("start_date")
            end_param = request.args.get("end_date")
            exam_type = request.args.get("exam_type")

            if not(start_param and end_param):

                return {"message": "Must provide both start and end time"}, 422

            try:
                start_date = datetime.strptime(request.args['start_date'], "%Y-%m-%d")
                end_date = datetime.strptime(request.args['end_date'], "%Y-%m-%d")

            except ValueError as err:
                print(err)
                return {"message", "Unable to return date time string"}, 422

            start_date = self.timezone.localize(start_date)

            end_date += timedelta(days=1)

            end_date = self.timezone.localize(end_date)

            exams = Exam.query.filter_by(office_id=csr.office_id) \
                              .join(Booking, Exam.booking_id == Booking.booking_id) \
                              .filter(Booking.start_time >= start_date) \
                              .filter(Booking.start_time < end_date) \
                              .join(Invigilator, Booking.invigilator_id == Invigilator.invigilator_id) \
                              .join(Room, Booking.room_id == Room.room_id) \
                              .join(Office, Booking.office_id == Office.office_id) \
                              .join(ExamType, Exam.exam_type_id == ExamType.exam_type_id)

            if exam_type == '1':
                exams = exams.filter(ExamType.ita_ind == 1)
            elif exam_type == '2':
                exams = exams.filter(ExamType.exam_type_name == 'Veterinary Exam')
            elif exam_type == '3':
                exams = exams.filter(ExamType.exam_type_name == 'Milk Grader')
            elif exam_type == '4':
                exams = exams.filter(ExamType.exam_type_name == 'Pesticide')

            dest = io.StringIO()
            out = csv.writer(dest)
            out.writerow(['Office Name', 'Exam Type', 'Exam ID', 'Exam Name', 'Examinee Name', 'Event ID', 'Room Name', 'Invigilator Name', 'Booking ID', 'Booking Name', 'Exam Received', 'Exam Returned' ])

            for exam in exams:
                out.writerow([exam.office.office_name, exam.exam_type.exam_type_name, exam.exam_id, exam.exam_name, exam.examinee_name,
                              exam.event_id, exam.booking.room.room_name, exam.booking.invigilator.invigilator_name,
                              exam.booking.booking_id, exam.booking.booking_name, exam.exam_returned_ind,
                              exam.exam_returned_ind ])

            output = make_response(dest.getvalue())
            output.headers["Content-Disposition"] = "attachment; filename=export.csv"
            output.headers["Content-type"] = "text/csv"

            return output

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {"message": "api is down"}, 500