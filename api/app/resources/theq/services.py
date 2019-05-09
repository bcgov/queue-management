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

from functools import cmp_to_key
from flask import request
from flask import g
from flask_restplus import Resource

from qsystem import db
from qsystem import api, oidc
from app.models.theq import Service
from app.models.theq import Office
from app.models.theq import ServiceReq, Citizen, CSR
from sqlalchemy import exc
from app.schemas.theq import ServiceSchema, OfficeSchema


@api.route("/services/refresh/", methods=["GET"])
class Refresh(Resource):
    """
    Refresh the quick lists to the 5 most frequently used items.
    Returns the resulting office object with updated lists indicated.
    """
    def get(self):
        if request.args.get('office_id'):
            office_id = int(request.args.get('office_id'))

            csr = CSR.find_by_username(g.jwt_oidc_token_info['preferred_username'])
            
            if csr.role.role_code == "GA":
            
                if csr.office_id != office_id:
                    return {'message': 'This is not your office, cannot refresh.'}, 403
            
            elif csr.role.role_code != "SUPPORT":
                return {'message': 'You do not have permission to view this end-point'}, 403
            
            back_office = Service.query.filter(Service.service_name=='Back Office')[0]
            def top_reqs(is_back_office=True):
                '''
                Get top requests for the office, and set the lists based on those.
                '''
                results = ServiceReq.query.join(
                    Citizen
                ).join(
                    Service
                ).filter(
                    Citizen.office_id == office_id,
                )
                if is_back_office:
                    results = results.filter(
                        Service.parent_id == back_office.service_id,
                        Service.display_dashboard_ind == 0,
                    )
                else:
                    results = results.filter(
                        Service.parent_id != back_office.service_id,
                        Service.display_dashboard_ind == 1,
                    )
                results = results.order_by(
                    ServiceReq.sr_id.desc()
                ).limit(100)

                # Some fancy dicts to collect the top 5 services in a list.
                counts = {}
                services = {}
                for result in results:
                    service_ct = counts.get(result.service_id, 0)
                    counts[result.service_id] = service_ct + 1
                    services[result.service_id] = result

                counts = list(counts.items())[-5:]
                counts.sort(key=lambda x: x[1]) # sort by quantity.
                service_ids = [c[0] for c in counts]
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

    @oidc.accept_token(require_token=True)
    def get(self):
        if request.args.get('office_id'):
            try:
                office_id = int(request.args['office_id'])
                office = Office.query.get(office_id)
                services = sorted(office.services, key=cmp_to_key(self.sort_services))
                filtered_services = [s for s in services if s.deleted is None]
                result = self.service_schema.dump(filtered_services)
                
                return {'services': result.data,
                        'errors': result.errors}

            except exc.SQLAlchemyError as e:
                print(e)
                return {'message': 'API is down'}, 500

            except ValueError as e:
                return {'message': 'office_id must be an integer.'}, 400
        else:
            try:
                services = Service.query.filter_by(actual_service_ind=1).all()
                result = self.services_schema.dump(services)
                return {'services': result.data,
                        'errors': result.errors}

            except exc.SQLAlchemyError as e:
                print(e)
                return {'message': 'api is down'}, 500
