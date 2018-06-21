from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, String

class CSRState(Base):

    csr_state_id    = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    csr_state_name  = db.Column(db.String(50), nullable=False)
    csr_state_desc  = db.Column(db.String(1000), nullable=False)

    csrs            = db.relationship('CSR', backref='csr_state', lazy=False)

    def __repr__(self, csr_state_name):
        return '<CSR State Name %r >' % self.csr_state_name

    def __init__(self, **kwargs):
        super(CSRState, self).__init__(**kwargs)
