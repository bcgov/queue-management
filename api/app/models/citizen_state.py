from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, String

class CitizenState(Base):

    model = api.model('CitizenState', {
        'cs_id' : fields.Integer,
        'cs_state_name' : fields.String,
        'cs_state_desc' : fields.String
        })

    cs_id           = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    cs_state_name   = db.Column(db.String(100))
    cs_state_desc   = db.Column(db.String(1000))

    def __repr__(self, cs_state_name):
        return '<CS State Name: %r>' % self.cs_state_name

    def __init__(self,cs_state_name, cs_state_desc):
        self.cs_state_name = cs_state_name
        self.cs_state_desc = cs_state_desc

    def json(self, cs_id, cs_state_name, cs_state_desc):
        return {"cs_id" : self.cs_id, 
                "cs_state_name" : self.cs_state_name, 
                "cs_state_desc" : self.cs_state_desc}