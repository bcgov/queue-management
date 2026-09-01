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
from collections.abc import Mapping

from marshmallow import EXCLUDE

from qsystem import ma


class BaseSchema(ma.SQLAlchemySchema):

    class Meta:
        load_instance = True
        unknown = EXCLUDE

    def validate(self, data, *, many=None, partial=None):
        """Support legacy validation calls that pass ORM instances."""
        if many is None:
            many = self.many

        if isinstance(data, Mapping):
            return super().validate(data, many=many, partial=partial)

        if isinstance(data, (list, tuple)):
            if all(isinstance(item, Mapping) for item in data):
                return super().validate(data, many=many, partial=partial)
            return {}

        return {} if data is not None else super().validate(data, many=many, partial=partial)
