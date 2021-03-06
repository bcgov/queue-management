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

from marshmallow import fields
from app.models.theq import ServiceReq
from app.schemas.theq import ChannelSchema, SRStateSchema, ServiceSchema, PeriodSchema
from qsystem import ma
from app.schemas import BaseSchema


class ServiceReqSchema(BaseSchema):

    class Meta(BaseSchema.Meta):
        model = ServiceReq
        include_relationships = True

    sr_id = fields.Int()
    citizen_id = fields.Int()
    channel_id = fields.Int()
    service_id = fields.Int()
    quantity = fields.Int()
    sr_number = fields.Int()
    periods = fields.Nested(PeriodSchema(exclude=('reception_csr_ind', 'sr', 'sr_id',)), many=True)
    sr_state = fields.Nested(SRStateSchema(exclude=('sr_state_id', 'sr_state_desc',)))
    service = fields.Nested(ServiceSchema(exclude=('actual_service_ind', 'deleted', 'display_dashboard_ind', 'prefix',
                                                   'service_code', 'service_desc', 'service_id',)))
    channel = fields.Nested(ChannelSchema(exclude=('channel_id',)))
    citizen = fields.Nested('CitizenSchema', exclude=('service_reqs',))
