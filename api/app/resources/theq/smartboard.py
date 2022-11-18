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
from qsystem import api
from app.models.theq import Citizen, CitizenState, ServiceReq, Office, Period
from app.models.theq import Office
from app.schemas.theq.period_schema import PeriodSchema
from app.schemas.theq import OfficeSchema
from sqlalchemy import exc
from sqlalchemy.orm import raiseload, joinedload
from sqlalchemy.dialects import postgresql

@api.route("/smartboard/", methods=["GET"])
class Smartboard(Resource):

    period_schema = PeriodSchema(exclude=('csr', 'csr_id', 'reception_csr_ind', 'sr', 'sr_id',))

    def get(self):
        try:
            citizens_waiting = []
            office_number = int(request.args.get('office_number'))

            office = Office.query.filter_by(office_number=office_number).first()

            if not office:
                return {'message': 'office_number could not be found.'}, 400
        
            if office.currently_waiting == 1 or office.show_currently_waiting_bottom == 1:
                citizens = Citizen.query \
                    .options(joinedload(Citizen.service_reqs, innerjoin=True).options(joinedload(ServiceReq.periods).options(raiseload(Period.csr),raiseload(Period.sr))), raiseload(Citizen.cs),raiseload(Citizen.counter),raiseload(Citizen.user)) \
                    .filter_by(office_id=office.office_id) \
                    .filter_by(cs_id=active_citizen_state) 

                for c in citizens:
                    active_service_request = c.get_active_service_request()

                    #  Make sure a category, rather than a service, hasn't slipped in somehow.
                    if active_service_request and active_service_request.service.parent:

                        # Filter Back Office out of services
                        if active_service_request.service.parent.service_name == "Back Office":
                            continue

                        active_period = active_service_request.get_active_period()
                        period = self.period_schema.dump(active_period)

                        citizens_waiting.append({
                            "ticket_number": c.ticket_number,
                            "active_period": period
                        })
                    else:
                        #  Display error to console, no other action taken.
                        print("==> Error in Smartboard: Citizen has no active service request. " \
                                + "Possible cause, category, not service, selected.")
    
            return {
                "office_type": office.sb.sb_type,
                "citizens": citizens_waiting
            }

        except exc.SQLAlchemyError as exception:
            logging.exception(exception)
            return {'message': 'API is down'}, 500
        except TypeError as exception:
            logging.exception(exception)
            return {'message': 'office_number must be an integer.'}, 400
        except ValueError as exception:
            logging.exception(exception)
            return {'message': 'office_number must be an integer.'}, 400


@api.route("/smardboard/side-menu/<string:id>", methods=["GET"])
class SmartBoradQMenu(Resource):
    office_schema = OfficeSchema()

    def get(self, id):
        try:
            # get office details from url id
            office = Office.query.filter_by(office_number=id).first()
            if not office:
                return {'message': 'office_number could not be found.'}, 400
            else:
                return {'office': self.office_schema.dump(office)}, 200
        except exc.SQLAlchemyError as exception:
            logging.exception(exception)
            return {'message': 'API is down'}, 500

try:
    citizen_state = CitizenState.query.filter_by(cs_state_name="Active").first()
    active_citizen_state = citizen_state.cs_id
except Exception as ex:
    active_citizen_state = 1
    print("==> In smartboard.py")
    print("    --> NOTE!!  You should only see this if doing a 'python3 manage.py db upgrade'")