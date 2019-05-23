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
from app.models.theq import Channel
from app.schemas.theq import ChannelSchema
from sqlalchemy import exc


@api.route("/channels/", methods=["GET"])
class ChannelList(Resource):

    channels_schema = ChannelSchema(many=True)

    @oidc.accept_token(require_token=True)
    def get(self):
        try:
            channels = Channel.query.all()
            result = self.channels_schema.dump(channels)
            return {'channels': result.data,
                    'errors': result.errors}, 200

        except exc.SQLAlchemyError as e:
            print (e)
            return {"message": "api is down"}, 500
