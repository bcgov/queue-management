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

from qsystem import db
from app.models.theq import Base


class SmartBoard(Base):

    sb_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    sb_type = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return self.sb_type

    def __init__(self, **kwargs):
        super(SmartBoard, self).__init__(**kwargs)
