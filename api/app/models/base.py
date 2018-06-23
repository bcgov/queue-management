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
        print ("Saving to db!")
        session.add(self)

    def save(self):
        print ("saving!")
        run_transaction(sessionmaker, self.save_to_db)
    
    @classmethod
    def get_by_id(cls, id):
        
        def callback(session):

            obj = session.query(cls).get(id)
            session.expunge(obj)

            return obj

        return run_transaction(sessionmaker, callback)
