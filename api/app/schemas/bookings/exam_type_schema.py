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
import toastedmarshmallow
from app.models.bookings import ExamType
from qsystem import ma


class ExamTypeSchema(ma.ModelSchema):

    class Meta:
        model = ExamType
        exclude = ("exam",)
        jit = toastedmarshmallow.Jit

    exam_type_id = fields.Int(dump_only=True)
    exam_type_name = fields.Str()
    exam_color = fields.Str()
    number_of_hours = fields.Int()
    method_type = fields.Str()
    ita_ind = fields.Int()
