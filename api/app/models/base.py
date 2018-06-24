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

from flask_restplus import fields
from qsystem import api, db, sessionmaker
from sqlalchemy.ext.declarative import declared_attr
from cockroachdb.sqlalchemy import run_transaction

class Base(db.Model, object):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def save_to_db(self, session):
        session.add(self)

    def save(self):
        run_transaction(sessionmaker, self.save_to_db)
    
    @classmethod
    def get_by_id(cls, id, remove_from_session=False):

        def callback(session):
            obj = session.query(cls).get(id)
            if remove_from_session:
                session.expunge(obj)
            return obj

        return run_transaction(sessionmaker, callback)
