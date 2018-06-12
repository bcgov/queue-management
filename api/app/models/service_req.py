from flask_restplus import fields
from qsystem import api, db
from base import Base 

class ServiceReqTable(MyBase, Base, db.model):

    model = api.model('ServiceReqTable' {
        'sr_id' : fields.Integer,
        'citizen_id' : fields.Integer,
        'quantity' : fields.Integer,
        'service_id' : fields.Integer,
        'sr_state_id' :  fields.Integer
        })

    sr_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    citizen_id = db.Column(db.BigInteger)
    quantity =  db.Column(db.Integer)
    service_id = db.Column(db.BigInteger)
    sr_state_id = db.Column(db.BigInteger)

    # TODO is repr needed for testing?

    def __init__(self, sr_id, citizen_id, quantity, service_id, sr_state_id):
        self.sr_id = sr_id
        self.citizen_id = citizen_id
        self.quantity = quantity
        self.service_id = service_id
        self.sr_state_id

    def json(self, sr_id, citizen_id, quantity, service_id, sr_state_id):
        return {"sr_id" : self.sr_id, "citizen_id" : self.citizen_id, "quantity" : self.quantity, 
                "service_id" : self.service_id, "sr_state_id" : self.sr_state_id}