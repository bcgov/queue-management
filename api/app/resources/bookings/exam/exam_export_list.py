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
from qsystem import api, jwt
from datetime import datetime, timedelta
import pytz
import csv
import io


@api.route("/exams/export/", methods=["GET"])
class ExamList(Resource):

    exam_schema = ExamSchema(many=True)

    timezone = pytz.timezone("US/Pacific")

    @jwt.requires_auth
    def get(self):

        print("==> In Python GET /exams/export/ endpoint")

        try:
            csr = CSR.find_by_username(g.jwt_oidc_token_info['preferred_username'])

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
                              .join(Invigilator, Booking.invigilator_id == Invigilator.invigilator_id, isouter=True) \
                              .join(Room, Booking.room_id == Room.room_id, isouter=True) \
                              .join(Office, Booking.office_id == Office.office_id) \
                              .join(ExamType, Exam.exam_type_id == ExamType.exam_type_id)

            if exam_type == 'ita':
                exams = exams.filter(ExamType.ita_ind == 1)
            elif exam_type == 'all_non_ita':
                exams = exams.filter(ExamType.ita_ind == 0)

            dest = io.StringIO()
            out = csv.writer(dest)
            out.writerow(['Office Name', 'Exam Type', 'Exam ID', 'Exam Name', 'Examinee Name', 'Event ID', 'Room Name',
                          'Invigilator Name', 'Booking ID', 'Booking Name', 'Exam Received', 'Exam Returned'])

            keys = [
                "office_name",
                "exam_type_name",
                "exam_id",
                "exam_name",
                "examinee_name",
                "event_id",
                "room_name",
                "invigilator_name",
                "booking_id",
                "booking_name",
                "exam_received_date",
                "exam_returned_ind"
            ]

            for exam in exams:
                row = []
                try:
                    for key in keys:
                        if key == "office_name":
                            row.append(exam.office.office_name)
                        elif key == "exam_type_name":
                            row.append(exam.exam_type.exam_type_name)
                        elif key == "exam_id":
                            row.append(exam.exam_id)
                        elif key == "exam_name":
                            row.append(exam.exam_name)
                        elif key == "examinee_name":
                            row.append(exam.examinee_name)
                        elif key == "event_id":
                            row.append(exam.event_id)
                        elif key == "room_name":
                            if exam.exam_type.group_exam_ind == 1:
                                row.append("")
                            else:
                                row.append(exam.booking.room.room_name)
                        elif key == "invigilator_name":
                            if exam.booking.invigilator is None:
                                row.append("")
                            else:
                                row.append(exam.booking.invigilator.invigilator_name)
                        elif key == "booking_id":
                            row.append(exam.booking.booking_id)
                        elif key == "booking_name":
                            row.append(exam.booking.booking_name)
                        elif key == "exam_received_date":
                            if exam.exam_received_date is None:
                                row.append("N")
                            else:
                                row.append("Y")
                        elif key == "exam_returned_ind":
                            if exam.exam_returned_ind == 0:
                                row.append("N")
                            else:
                                row.append("Y")

                    out.writerow(row)

                except AttributeError as error:
                    logging.error(error, exc_info=True)
                    return {"message": "Issue writing row to CSV ",
                            "key": key}, 500

            output = make_response(dest.getvalue())
            output.headers["Content-Disposition"] = "attachment; filename=export.csv"
            output.headers["Content-type"] = "text/csv"

            return output

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {"message": "api is down"}, 500
