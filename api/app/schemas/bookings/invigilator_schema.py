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
from qsystem import ma
import toastedmarshmallow
from app.models.bookings import Invigilator
from app.schemas.theq import OfficeSchema


class InvigilatorSchema(ma.ModelSchema):

    class Meta:
        model = Invigilator
        exclude = ("exams",)
        jit = toastedmarshmallow.Jit

    contact_phone = fields.Str()
    contact_email = fields.Str()
    contract_number = fields.Str()
    contract_expiry_date = fields.Str()
    invigilator_id = fields.Int(dump_only=True)
    invigilator_name = fields.Str()
    invigilator_notes = fields.Str()

    office = fields.Nested(OfficeSchema())
