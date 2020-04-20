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

from app.models.theq import Base, Citizen
from qsystem import cache, db
from app.models.bookings.appointments import Appointment


class PublicUser(Base):

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(100), unique=True, index=True)
    last_name = db.Column(db.String(100))
    display_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    telephone = db.Column(db.String(20))

    format_string = 'public_user_%s'

    def __repr__(self):
        return '<Public User Name:(name={self.display_name!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(PublicUser, self).__init__(**kwargs)

    @classmethod
    def find_by_username(cls, username):
        """Find User records by username."""
        key = PublicUser.format_string % username
        if cache.get(key):
            return cache.get(key)

        user = cls.query.filter_by(username=username).one_or_none()

        cache.set(key, user)
        return user

    @classmethod
    def find_appointments_by_username(cls, username: str):
        """Find all appointments for the user."""
        query = db.session.query(Appointment) \
            .join(Citizen) \
            .join(PublicUser) \
            .filter(PublicUser.username == username, Citizen.user_id == PublicUser.user_id)

        return query.all()
