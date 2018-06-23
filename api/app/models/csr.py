from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, Integer, String, Binary, DateTime

class CSR(Base):

    csr_id              = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username            = db.Column(db.String(150), nullable=False)
    office_id           = db.Column(db.Integer, db.ForeignKey('office.office_id'), nullable=False)
    role_id             = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable=False)
    qt_xn_csr_ind       = db.Column(db.Integer, nullable=False)
    receptionist_ind    = db.Column(db.Integer, nullable=False)
    deleted             = db.Column(db.DateTime, nullable=True)
    csr_state_id        = db.Column(db.Integer, db.ForeignKey('csrstate.csr_state_id'), nullable=False)

    periods             = db.relationship('Period', backref='csr', lazy=False)

    def __repr__(self):
        return '<CSR Username:(name={self.username!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(CSR, self).__init__(**kwargs)
