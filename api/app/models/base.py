from flask_restplus import fields
from qsystem import api, db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction

class Base(db.Model, object):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def save_to_db(self, session):
        session.add(self)

    def save(self):
        sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)
        run_transaction(sessionmaker, self.save_to_db)

    def get_by_id(self, id):
        run_transaction(self.query.get(id))
