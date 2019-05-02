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

import toastedmarshmallow
from marshmallow import fields
from app.models.theq import Period
from app.schemas.theq import PeriodStateSchema, ChannelSchema, CSRSchema
from qsystem import ma


class PeriodSchema(ma.ModelSchema):

    class Meta:
        model = Period
        jit = toastedmarshmallow.Jit

    period_id = fields.Int()
    sr_id = fields.Int()
    csr_id = fields.Int()
    reception_csr_ind = fields.Int()
    ps_id = fields.Int()
    time_start = fields.DateTime()
    time_end = fields.DateTime()
    ps = fields.Nested(PeriodStateSchema(exclude=('ps_id', 'ps_desc', 'ps_number',)))
    sr = fields.Nested("ServiceReqSchema", exclude=('periods',))
    csr = fields.Nested(CSRSchema(exclude=('csr_id', 'csr_state', 'csr_state_id', 'deleted', 'office', 'office_id',
                                           'periods', 'qt_xn_csr_ind', 'receptionist_ind', 'role', 'role_id')))
