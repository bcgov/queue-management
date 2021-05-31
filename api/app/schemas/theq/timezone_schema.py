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
from app.models.theq import Timezone
from qsystem import ma
from app.schemas import BaseSchema


class TimezoneSchema(BaseSchema):

    class Meta(BaseSchema.Meta):
        model = Timezone
        include_relationships = True

    timezone_id = fields.Int()
    timezone_name = fields.Str()
