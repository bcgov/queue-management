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

from flask import request
from flask_restplus import Resource
from qsystem import api
from app.models.theq import Citizen, CitizenState, ServiceReq, SRState
from app.models.theq import Office
from app.schemas.theq.period_schema import PeriodSchema
from sqlalchemy import exc


@api.route("/smartboard/", methods=["GET"])
class Smartboard(Resource):

    period_schema = PeriodSchema(exclude=('csr', 'csr_id', 'reception_csr_ind', 'request_periods', 'sr', 'sr_id',))

    def get(self):
        try:
            office_number = int(request.args.get('office_number'))

            office = Office.query.filter_by(office_number=office_number).first()

            if not office:
                return {'message': 'office_number could not be found.'}, 400

            active_citizen_state = CitizenState.query.filter_by(cs_state_name="Active").first()

            citizens = Citizen.query.filter_by(office_id=office.office_id) \
                .filter_by(cs_id=active_citizen_state.cs_id) \
                .join(ServiceReq, aliased=True)

            citizens_waiting = []

            for c in citizens:
                active_service_request = c.get_active_service_request()

                # Filter Back Office out of services
                if active_service_request.service.parent.service_name == "Back Office":
                    continue

                active_period = active_service_request.get_active_period()
                period = self.period_schema.dump(active_period)

                citizens_waiting.append({
                    "ticket_number": c.ticket_number,
                    "active_period": period.data
                })

            return {
                "office_type": office.sb.sb_type,
                "citizens": citizens_waiting
            }

        except exc.SQLAlchemyError as e:
            print(e)
            return {'message': 'API is down'}, 500
        except TypeError as e:
            print(e)
            return {'message': 'office_number must be an integer.'}, 400
        except ValueError as e:
            print(e)
            return {'message': 'office_number must be an integer.'}, 400

