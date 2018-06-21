from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, Integer

class ServiceReq(Base):

    model = api.model('ServiceReq', {
        'sr_id': fields.Integer,
        'citizen_id': fields.Integer,
        'quantity': fields.Integer,
        'service_id': fields.Integer,
        'sr_state_id':  fields.Integer
        })

    sr_id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    citizen_id  = db.Column(db.Integer, db.ForeignKey('citizen.citizen_id'))
    quantity    = db.Column(db.Integer)
    service_id  = db.Column(db.Integer, db.ForeignKey('service.service_id'))
    sr_state_id = db.Column(db.Integer, db.ForeignKey('srstate.sr_state_id'))

    periods     = db.relationship('Period', backref='service_req', lazy=False)

    def __init__(self, **kwargs):
        super(ServiceReq, self).__init__(**kwargs)

    def json(self, sr_id, citizen_id, quantity, service_id, sr_state_id):
        return {"sr_id" : self.sr_id, 
                "citizen_id" : self.citizen_id, 
                "quantity" : self.quantity, 
                "service_id" : self.service_id, 
                "sr_state_id" : self.sr_state_id}