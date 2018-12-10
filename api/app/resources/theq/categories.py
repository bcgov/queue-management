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


from flask_restplus import Resource
from qsystem import api, oidc
from app.models.theq import Service
from sqlalchemy import exc
from app.schemas.theq import ServiceSchema


@api.route("/categories/", methods=["GET"])
class Categories(Resource):

    categories_schema = ServiceSchema(many=True)

    @oidc.accept_token(require_token=True)
    def get(self):
        try:
            services = Service.query.filter_by(actual_service_ind=0).order_by(Service.service_name).all()
            result = self.categories_schema.dump(services)
            return {'categories': result.data,
                    'errors': result.errors}, 200

        except exc.SQLAlchemyError as e:
            print(e)
            return {"message": "API is down"}, 500
