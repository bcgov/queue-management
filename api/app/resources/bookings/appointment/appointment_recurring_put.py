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
from flask import request
from flask_restx import Resource
from qsystem import api, db, socketio, application
from app.models.bookings import Appointment
from app.models.theq import CSR, Office
from app.schemas.bookings import AppointmentSchema
from app.utilities.auth_util import Role, get_username
from app.auth.auth import jwt
from app.utilities.timezone_utils import convert_local_fields_to_utc


@api.route("/appointments/recurring/<string:id>", methods=["PUT"])
class AppointmentRecurringPut(Resource):

    appointment_schema = AppointmentSchema()

    @jwt.has_one_of_roles([Role.internal_user.value])
    def put(self, id):

        csr = CSR.find_by_username(get_username())

        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data received for updating an series of appointments"}

        if json_data.get('start_time') or json_data.get('end_time'):
            office = db.session.get(Office, csr.office_id)
            convert_local_fields_to_utc(json_data, office.timezone.timezone_name)

        appointments = Appointment.query.filter_by(recurring_uuid=id)\
                                  .filter_by(office_id=csr.office_id)\
                                  .all()

        for appointment in appointments:

            appointment = self.appointment_schema.load(json_data, instance=appointment, partial=True)
            warning = self.appointment_schema.validate(json_data)

            if warning:
                logging.warning('WARNING: %s', warning)
                return {"message": warning}, 422

            db.session.add(appointment)

        db.session.commit()

        result = self.appointment_schema.dump(appointments, many=True)

        if not application.config['DISABLE_AUTO_REFRESH']:
            socketio.emit('appointment_update', result, room=csr.office.office_name)

        return {
            "appointments": result,
            "errors": self.appointment_schema.validate(appointments)
        }, 200
