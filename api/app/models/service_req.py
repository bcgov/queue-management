from flask_restplus import fields
from qsystem import api, db
from base import Base 

class ServiceReq(Base):

    model = api.model('ServiceReq' {
        'sr_id' : fields.Integer,
        'citizen_id' : fields.Integer,
        'quantity' : fields.Integer,
        'service_id' : fields.Integer,
        'sr_state_id' :  fields.Integer
        })

    sr_id       = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    citizen_id  = db.Column(db.BigInteger, ForeignKey('citizen.citizen_id'))
    quantity    =  db.Column(db.Integer)
    service_id  = db.Column(db.BigInteger, ForeignKey('service.service_id'))
    sr_state_id = db.Column(db.BigInteger, ForeignKey('srstate.sr_state_id'))

    citizen     = db.relationship("Citizen")
    service     = db.relationship("Service")
    sr_state    = db.relationship("SR_State") 

    def __init__(self, sr_id, citizen_id, quantity, service_id, sr_state_id):
        self.sr_id          = sr_id
        self.citizen_id     = citizen_id
        self.quantity       = quantity
        self.service_id     = service_id
        self.sr_state_id    = sr_state_id

    def json(self, sr_id, citizen_id, quantity, service_id, sr_state_id):
        return {"sr_id" : self.sr_id, 
                "citizen_id" : self.citizen_id, 
                "quantity" : self.quantity, 
                "service_id" : self.service_id, 
                "sr_state_id" : self.sr_state_id}