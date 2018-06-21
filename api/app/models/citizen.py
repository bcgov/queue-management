from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, Integer, String
from marshmallow import fields

class Citizen(Base):

    citizen_id          = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    office_id           = db.Column(db.Integer, db.ForeignKey('office.office_id'), nullable=False)
    ticket_number       = db.Column(String(50), nullable=False)
    citizen_name        = db.Column(String(150), nullable=True)
    citizen_comments    = db.Column(String(1000), nullable=True)
    qt_xn_citizen_ind   = db.Column(Integer, nullable=False)
    cs_id               = db.Column(BigInteger, db.ForeignKey('citizenstate.cs_id'), nullable=False)
    start_time          = db.Column(db.DateTime, nullable=False)

    service_reqs        = db.relationship('ServiceReq', backref='citizen', lazy=False)

    def __repr__(self, citizen_name):
        return '<Citizen: %r>' % self.citizen_name

    def __init__(self, **kwargs):
        super(Citizen, self).__init__(**kwargs)
