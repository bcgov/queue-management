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
from app.models.bookings import Room
from app.schemas.theq import OfficeSchema
from qsystem import ma
from app.schemas import BaseSchema


class RoomSchema(BaseSchema):

    class Meta(BaseSchema.Meta):
        model = Room
        include_relationships = True

    capacity = fields.Int()
    color = fields.Str()
    room_id = fields.Int(dump_only=True)
    room_name = fields.Str()
    deleted = fields.Str()

    office = fields.Nested(OfficeSchema())
