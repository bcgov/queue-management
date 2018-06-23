from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from datetime import datetime

class Citizen(Base):

    citizen_id          = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    office_id           = db.Column(db.Integer, db.ForeignKey('office.office_id'), nullable=False)
    ticket_number       = db.Column(db.String(50), nullable=False)
    citizen_name        = db.Column(db.String(150), nullable=True)
    citizen_comments    = db.Column(db.String(1000), nullable=True)
    qt_xn_citizen_ind   = db.Column(db.Integer, default=0, nullable=False)
    cs_id               = db.Column(db.BigInteger, db.ForeignKey('citizenstate.cs_id'), nullable=False)
    start_time          = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    service_reqs        = db.relationship('ServiceReq', backref='citizen', lazy=False)

    def __repr__(self):
        return '<Citizen Name:(name={self.citizen_name!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(Citizen, self).__init__(**kwargs)
        self.ticket_number = 'A1'
