from flask_restplus import fields
from qsystem import api, db
from base import Base 

class SRStateTable(MyBase, Base, db.model):

    model = api.model('SRStateTable' {
        'sr_state_id' : fields.Integer,
        'sr_code' : fields.String,
        'sr_state_desc' fields,String
        })

    sr_state_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    sr_code = db.Column(db.String(100))
    sr_state_desc = db.Column(db.String(1000))

    def __repr__(self, sr_code):
        return '<SR Code: %r>' % self.sr_code   

    def __init__(self, sr_state_id, sr_code, sr_state_desc):
        self.sr_state_id = sr_state_id
        self.sr_code = sr_code
        self.sr_state_desc  =  sr_state_desc

    def json(self, sr_state_id, sr_code, sr_state_desc):
        return {"sr_state_id" : self.sr_state_id, "sr_code" : self.sr_code, "sr_state_desc" : self.sr_state_desc}