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
from flask import request, jsonify
from flask_restx import Resource
from sqlalchemy import exc
from qsystem import api, db, oidc
from app.models.bookings import Invigilator
from app.schemas.bookings import InvigilatorSchema


@api.route("/invigilator/<int:id>/", methods=["PUT"])
class InvigilatorPut(Resource):

    invigilator_schema = InvigilatorSchema()

    @oidc.accept_token(require_token=True)
    def put(self, id):

        try:
            add_param = request.args.get("add")
            subtract_param = request.args.get("subtract")

            validate_params(add_param, subtract_param)

            invigilator = Invigilator.query.filter_by(invigilator_id=id).first_or_404()
            invigilator_shadow_count = invigilator.shadow_count
            invigilator_shadow_flag = invigilator.shadow_flag

            if add_param == 'True' and subtract_param == 'False':
                if invigilator_shadow_count == 0 and invigilator_shadow_flag == 'N':
                    invigilator_shadow_count += 1
                elif invigilator_shadow_count == 1 and invigilator_shadow_flag == 'N':
                    invigilator_shadow_count += 1
                    invigilator_shadow_flag = 'Y'
                else:
                    return {"message": "Invigilator data is not correct in order to Add."}, 422
            elif subtract_param == 'True' and add_param == 'False':
                if invigilator_shadow_count > 0 and invigilator_shadow_count <= 2:
                    if invigilator_shadow_flag == 'Y':
                        invigilator_shadow_flag = 'N'
                        invigilator_shadow_count -= 1
                    else:
                        invigilator_shadow_count -= 1
                elif invigilator_shadow_count == 0:
                    invigilator_shadow_count = 0
                    invigilator_shadow_flag = 'N'
                else:
                    return {"message": "Invigilator data is outside of range to subtract."}, 422

            data = {}
            data['shadow_count'] = invigilator_shadow_count
            data['shadow_flag'] = invigilator_shadow_flag

            invigilator, warning = self.invigilator_schema.load(data, instance=invigilator, partial=True)

            if warning:
                logging.warning("WARNING: %s", warning)
                return {"message": warning}, 422

            db.session.add(invigilator)
            db.session.commit()

            result = self.invigilator_schema.dump(invigilator)

            return {"invigilator": result.data,
                    "errors": result.errors}, 200

        except exc.SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            return {"message": "API is down."}, 500


def validate_params(add_param, subtract_param):

    if add_param and subtract_param:
        return {"message": "Both Add and Subtract parameters are set to TRUE. Please pick either Add OR Subtract"}, 422
    elif not add_param and not subtract_param:
        return {"message": "Both Add and Subtract parameters are set to FALSE. Please pick either Add OR Subtract"},
