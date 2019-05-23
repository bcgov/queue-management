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

            is_designate = csr.finance_designate

            start_param = request.args.get("start_date")
            end_param = request.args.get("end_date")
            exam_type = request.args.get("exam_type")

            validate_params(start_param, end_param)

            try:
                start_date = datetime.strptime(request.args['start_date'], "%Y-%m-%d")
                end_date = datetime.strptime(request.args['end_date'], "%Y-%m-%d")

            except ValueError as err:
                print(err)
                return {"message", "Unable to return date time string"}, 422

            start_date = self.timezone.localize(start_date)

            end_date += timedelta(days=1)

            end_date = self.timezone.localize(end_date)

            exams = Exam.query.join(Booking, Exam.booking_id == Booking.booking_id) \
                              .filter(Booking.start_time >= start_date) \
                              .filter(Booking.start_time < end_date) \
                              .join(Invigilator, Booking.invigilator_id == Invigilator.invigilator_id, isouter=True) \
                              .join(Room, Booking.room_id == Room.room_id, isouter=True) \
                              .join(Office, Booking.office_id == Office.office_id) \
                              .join(ExamType, Exam.exam_type_id == ExamType.exam_type_id)

            non_exams = Booking.query.join(Exam, Booking.booking_id == Exam.booking_id, isouter=True) \
                                     .filter(Booking.start_time >= start_date) \
                                     .filter(Booking.start_time < end_date) \
                                     .filter(Exam.booking_id.is_(None)) \
                                     .join(Room, Booking.room_id == Room.room_id, isouter=True) \
                                     .join(Office,  Booking.office_id == Office.office_id) \

            if not is_designate:
                exams = exams.filter(Booking.office_id == csr.office_id)

            if exam_type == 'ita':
                exams = exams.filter(ExamType.ita_ind == 1)
            elif exam_type == 'all_non_ita':
                exams = exams.filter(ExamType.ita_ind == 0)

            dest = io.StringIO()
            out = csv.writer(dest)
            out.writerow(['Office Name', 'Exam Type', 'Exam ID', 'Exam Name', 'Examinee Name', 'Event ID', 'Room Name',
                          'Invigilator Name', 'SBC Invigilator', 'Start Time', 'End Time', 'Booking ID', 'Booking Name',
                          'Number Of Students', 'Exam Received', 'Exam Written', 'Exam Returned', 'Notes',
                          'Collect Fees'])

            keys = [
                "office_name",
                "exam_type_name",
                "exam_id",
                "exam_name",
                "examinee_name",
                "event_id",
                "room_name",
                "invigilator_name",
                "sbc_staff_invigilated",
                "start_time",
                "end_time",
                "booking_id",
                "booking_name",
                "number_of_students",
                "exam_received_date",
                "exam_written_ind",
                "exam_returned_date",
                "notes",
                "fees"
            ]

            exam_keys = [
                "exam_id",
                "exam_name",
                "examinee_name",
                "event_id",
                "number_of_students",
                "notes",
            ]

            booking_keys = [
                "start_time",
                "end_time",
                "booking_id",
                "booking_name"
            ]

            non_exam_keys = [
                "exam_name",
                "notes",
            ]

            for exam in exams:
                row = []
                try:
                    for key in keys:
                        if key == "room_name":
                            write_room(row, exam)
                        elif key == "invigilator_name":
                            write_invigilator(row, exam)
                        elif key == "sbc_staff_invigilated":
                            write_sbc(row, exam)
                        elif key == "exam_received_date":
                            write_exam_received(row, exam)
                        elif key == "exam_written_ind":
                            write_exam_written(row, exam)
                        elif key == "exam_returned_date":
                            write_exam_returned(row, exam)
                        elif key == "office_name":
                            row.append(getattr(exam.office, key))
                        elif key == "exam_type_name":
                            row.append(getattr(exam.exam_type, key))
                        elif key in booking_keys:
                            row.append(getattr(exam.booking, key))
                        elif key in exam_keys:
                            row.append(getattr(exam, key))
                        elif key == "fees":
                            row.append("")

                    out.writerow(row)

                except AttributeError as error:
                    logging.error(error, exc_info=True)
                    return {"message": "Issue writing row to CSV ",
                            "key": key}, 500

            for non_exam in non_exams:
                row = []
                try:
                    for key in keys:
                        if key == "room_name":
                            write_booking_room(row, non_exam)
                        elif key == "invigilator_name":
                            row.append("")
                        elif key == "sbc_staff_invigilated":
                            row.append("")
                        elif key == "exam_received_date":
                            row.append("")
                        elif key == "exam_written_ind":
                            row.append("")
                        elif key == "exam_returned_date":
                            row.append("")
                        elif key == "office_name":
                            row.append(getattr(non_exam.office, key))
                        elif key == "exam_type_name":
                            row.append("Non Exam Booking")
                        elif key in booking_keys:
                            row.append(getattr(non_exam, key))
                        elif key in non_exam_keys:
                            which_non_exam_key(non_exam, row, key)
                        elif key == "exam_id":
                            row.append("")
                        elif key == "exam_name":
                            row.append("")
                        elif key == "examinee_name":
                            row.append("")
                        elif key == "event_id":
                            row.append("")
                        elif key == "fees":
                            which_non_exam_key(non_exam, row, key)
                        elif key == "number_of_students":
                            row.append("")
                        elif key == "exam_received_ind":
                            row.append("")

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


def write_booking_room(row, booking):
    row.append(booking.room.room_name)


def write_room(row, exam):
    if exam.booking and exam.booking.room:
        row.append(exam.booking.room.room_name)
    else:
        row.append("")


def write_invigilator(row, exam):
    if exam.booking.invigilator is None:
        row.append("")
    else:
        row.append(exam.booking.invigilator.invigilator_name)


def write_sbc(row, exam):
    if exam.booking.sbc_staff_invigilated == 1:
        row.append("Y")
    else:
        row.append("N")


def write_exam_received(row, exam):
    if exam.exam_received_date is None:
        row.append("N")
    else:
        row.append("Y")


def write_exam_written(row, exam):
    if exam.exam_written_ind == 1:
        row.append("Y")
    else:
        row.append("N")


def write_exam_returned(row, exam):
    if exam.exam_returned_date is None:
        row.append("N")
    else:
        row.append("Y")


def validate_params(start_param, end_param):
    if not (start_param and end_param):
        return {"message": "Must provide both start and end time"}, 422


def write_non_exam_name(booking, row):
    row.append(getattr(booking, 'booking_name'))


def write_contact_info(booking, row):
    row.append(getattr(booking, 'booking_contact_information'))


def which_non_exam_key(booking, row, key):
    if key == 'exam_name':
        write_non_exam_name(booking, row)
    elif key == 'notes':
        write_contact_info(booking, row)
    elif key == 'start_time':
        row.append(getattr(booking.start_time, key))
    elif key == 'end_time':
        row.append(getattr(booking.end_time, key))
    elif key == 'fees':
        if booking.fees == 'false':
            row.append("N")
        elif booking.fees == 'true':
            row.append("Y")




