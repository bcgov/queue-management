from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, String

class SRState(Base):

    sr_state_id     = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    sr_code         = db.Column(db.String(100), nullable=False)
    sr_state_desc   = db.Column(db.String(1000), nullable=False)

    service_reqs    = db.relationship('ServiceReq', backref='sr_state', lazy=False)

    def __repr__(self):
        return '<SR State Code:(name={self.sr_code!r})>'.format(self=self)   

    def __init__(self, **kwargs):
        super(SRState, self).__init__(**kwargs)
