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
from app.models.theq import Office
from app.schemas.theq import SmartBoardSchema
from qsystem import ma


class OfficeSchema(ma.ModelSchema):

    class Meta:
        model = Office
        jit = toastedmarshmallow.Jit
        exclude = ('citizens', 'csrs', 'deleted', 'exams', 'rooms', 'services',)

    office_id = fields.Int()
    office_name = fields.Str()
    office_number = fields.Int()
    sb_id = fields.Int()
    deleted = fields.DateTime()

    sb = fields.Nested(SmartBoardSchema())
