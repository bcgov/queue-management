from flask_restplus import fields
from qsystem import api, db
from sqlalchemy.ext.declarative import declared_attr

class Base(db.Model, object):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()