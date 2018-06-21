from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, Integer

class ServiceReq(Base):

    sr_id       = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    citizen_id  = db.Column(db.Integer, db.ForeignKey('citizen.citizen_id'), nullable=False)
    quantity    = db.Column(db.Integer, nullable=False)
    service_id  = db.Column(db.Integer, db.ForeignKey('service.service_id'), nullable=False)
    sr_state_id = db.Column(db.Integer, db.ForeignKey('srstate.sr_state_id'), nullable=False)

    periods     = db.relationship('Period', backref='service_req', lazy=False)

    def __init__(self, **kwargs):
        super(ServiceReq, self).__init__(**kwargs)
