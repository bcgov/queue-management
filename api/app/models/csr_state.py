from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, String

class CSRState(Base):

    model = api.model('CSRState', {
        'csr_state_id' : fields.Integer,
        'csr_state_name' : fields.String,
        'csr_state_desc' : fields.String
        })

    csr_state_id    = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    csr_state_name  = db.Column(db.String(50))
    csr_state_desc  = db.Column(db.String(1000))

    def __repr__(self, csr_state_name):
        return '<CSR State Name %r >' % self.csr_state_name

    def __init__(self, csr_state_id, csr_state_name, csr_state_desc):
        self.csr_state_id   = csr_state_id
        self.csr_state_name = csr_state_name
        self.csr_state_desc = csr_state_desc

    def json(self, csr_state_id, csr_state_name, csr_state_desc):
        return {"csr_state_id" : self.csr_state_id, 
                "csr_state_name" : self.csr_state_name, 
                "csr_state_desc" : csr_state_desc}