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

from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import Period
from app.schemas import PeriodStateSchema, ChannelSchema
from qsystem import db

class PeriodSchema(ModelSchema):

    class Meta:
        model = Period
        sqla_session = db.session

    period_id           = fields.Int()
    sr_id               = fields.Int()
    csr_id              = fields.Int()
    reception_csr_ind   = fields.Int()
    channel_id          = fields.Int()
    ps_id               = fields.Int()
    time_start          = fields.DateTime()
    time_end            = fields.DateTime()
    accurate_time_ind   = fields.Integer()
    period_state        = fields.nested(PeriodStateSchema)
    channel             = fields.nested(ChannelSchema)