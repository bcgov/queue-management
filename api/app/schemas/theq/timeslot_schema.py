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
from app.models.theq import TimeSlot
from qsystem import ma
from app.schemas import BaseSchema


class TimeslotSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = TimeSlot
        include_relationships = True

    start_time = fields.Time()
    end_time = fields.Time()
    day_of_week = fields.List(fields.String)
    no_of_slots = fields.Integer()
    office = fields.Integer(attribute="office_id")
