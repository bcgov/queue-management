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

from qsystem import cache, db
from app.models.theq import Base


class SRState(Base):

    sr_state_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    sr_code = db.Column(db.String(100), nullable=False)
    sr_state_desc = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return '<SR State Code:(name={self.sr_code!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(SRState, self).__init__(**kwargs)

    @classmethod
    @cache.memoize(timeout=300)
    def get_state_by_name(cls, sr_code):
        state = SRState.query.filter_by(sr_code=sr_code).first()
        return state
