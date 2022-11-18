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
from functools import cmp_to_key
from flask import request
from flask import g
from flask_restx import Resource
from qsystem import api
from qsystem import db
from app.models.theq import Service
from app.models.theq import Office
from app.models.theq import ServiceReq, Citizen, CSR
from sqlalchemy import exc
from app.schemas.theq import ServiceSchema, OfficeSchema
from sqlalchemy.orm import noload, joinedload
from app.utilities.auth_util import Role, has_any_role
from app.auth.auth import jwt


@api.route("/services/refresh/", methods=["GET"])
class Refresh(Resource):
    """
    Refresh the quick lists to the 5 most frequently used items.
    Returns the resulting office object with updated lists indicated.
    """
    @jwt.has_one_of_roles([Role.internal_user.value])
    def get(self):
        if request.args.get('office_id'):
            office_id = int(request.args.get('office_id'))
            csr = CSR.find_by_username(g.jwt_oidc_token_info['username'])
            
            if csr.role.role_code == "GA":
            
                if csr.office_id != office_id:
                    return {'message': 'This is not your office, cannot refresh.'}, 403
            
            elif csr.role.role_code != "SUPPORT":
                return {'message': 'You do not have permission to view this end-point'}, 403
            
            def top_reqs(is_back_office=True):

                # Get top requests for the office, and set the lists based on those.
                
                results = ServiceReq.query.options(
                    noload('*'), joinedload('service')
                ).join(
                    Citizen
                ).join(
                    Service
                ).filter(
                    Citizen.office_id == office_id,
                ).filter(
                    Service.deleted.is_(None)
                )
                if is_back_office:
                    results = results.filter(
                        Service.display_dashboard_ind == 0,
                    )
                else:
                    results = results.filter(
                        Service.display_dashboard_ind == 1,
                    )
                results = results.order_by(
                    ServiceReq.sr_id.desc()
                ).limit(100)
                
                print("start *****************************")
                print(results.statement)
                print("end *****************************")

                # Some fancy dicts to collect the top 5 services in a list.
                counts = {}
                services = {}
                byname = {}
                for result in results:
                    service_ct = counts.get(result.service_id, 0)
                    counts[result.service_id] = service_ct + 1
                    services[result.service_id] = result
                    byname[result.service.service_name] = counts[result.service_id]
                
                counts = list(counts.items())
                counts.sort(key=lambda x: x[1]) # sort by quantity.
                counts = counts[-5:]

                print("Results of refresh call for office {} : {}".format(office_id, byname))

                service_ids = [c[0] for c in counts]

                print("List chosen: {}".format([r.service.service_name for r in services.values() if r.service_id in service_ids]))

                return [r.service for r in services.values() if r.service_id in service_ids]

            quick_list = top_reqs(is_back_office=False)
            back_office_list = top_reqs(is_back_office=True)

            office = Office.query.get(office_id)
            office.quick_list =  quick_list
            office.back_office_list = back_office_list
            db.session.commit()

            return OfficeSchema().dump(office)
        else:
            return {'message': 'no office specified'}, 400


@api.route("/services/", methods=["GET"])
class Services(Resource):

    service_schema = ServiceSchema(many=True)
    services_schema = ServiceSchema(many=True)

    @classmethod
    def sort_services(cls, a, b):
        if a.parent is None and b.parent is not None:
            return -1
        elif a.parent is not None and b.parent is None:
            return 1
        elif (a.parent is None and b.parent is None) or (a.parent == b.parent):
            if a.service_name.lower() < b.service_name.lower():
                return -1
            else:
                return 1
        else:
            if a.parent.service_name.lower() < b.parent.service_name.lower():
                return -1
            else:
                return 1

    def get(self):
        if request.args.get('office_id'):
            try:
                office_id = int(request.args['office_id'])
                office = Office.query.get(office_id)
                services = sorted(office.services, key=cmp_to_key(self.sort_services))
                filtered_services = [s for s in services if s.deleted is None]
                result = self.service_schema.dump(filtered_services)
                
                return {'services': result,
                        'errors': {}}

            except exc.SQLAlchemyError as exception:
                logging.exception(exception)
                return {'message': 'API is down'}, 500

            except ValueError as exception:
                return {'message': 'office_id must be an integer.'}, 400
        else:
            try:
                services = Service.query.filter_by(actual_service_ind=1).all()
                result = self.services_schema.dump(services)
                return {'services': result,
                        'errors': {}}

            except exc.SQLAlchemyError as exception:
                logging.exception(exception)
                return {'message': 'api is down'}, 500
