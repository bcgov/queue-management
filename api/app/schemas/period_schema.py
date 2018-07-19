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
from app.models import Period
from app.schemas import ChannelSchema, CSRSchema, PeriodStateSchema
from qsystem import ma


class PeriodSchema(ma.ModelSchema):

    class Meta:
        model = Period

    period_id = fields.Int()
    sr_id = fields.Int()
    csr_id = fields.Int()
    reception_csr_ind = fields.Int()
    ps_id = fields.Int()
    time_start = fields.DateTime()
    time_end = fields.DateTime()
    accurate_time_ind = fields.Integer()
    ps = fields.Nested(PeriodStateSchema, exclude=('ps_desc', 'ps_number',))
    csr = fields.Nested(CSRSchema)
