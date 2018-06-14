from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, Integer, String

# TODO Please review the valid state table to see for testing
class PeriodState(Base):

    model = api.model('PeriodState', {
        'ps_id' : fields.Integer,
        'ps_name' : fields.String,
        'ps_desc' : fields.String,
        'ps_number' : fields.Integer
        })

    ps_id   = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    ps_name = db.Column(db.String(100))
    ps_desc = db.Column(db.String(1000))
    ps_name = db.Column(db.Integer)

    def __repr__(self, ps_name):
        return '<Period State Name: %r>' % self.ps_name

    def __init__(self, ps_id, ps_name, ps_desc, ps_number):
        self.ps_id      = ps_id
        self.ps_name    = ps_name
        self.ps_desc    = ps_desc
        self.ps_number  = ps_number

    def json(self, ps_id, ps_name, ps_desc, ps_number):
        return {"ps_id" : self.ps_id, 
                "ps_name" : self.ps_name, 
                "ps_desc" : self.ps_desc, 
                "ps_number" : self.ps_number}