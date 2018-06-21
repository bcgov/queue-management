from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, Integer, DateTime

class Period(Base):

    period_id           = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    sr_id               = db.Column(db.Integer, db.ForeignKey('servicereq.sr_id'), nullable=False)
    csr_id              = db.Column(db.Integer, db.ForeignKey('csr.csr_id'), nullable=False)
    reception_csr_ind   = db.Column(db.Integer, nullable=False)
    channel_id          = db.Column(db.Integer, db.ForeignKey('channel.channel_id'), nullable=False)
    ps_id               = db.Column(db.Integer, db.ForeignKey('periodstate.ps_id'), nullable=False)
    time_start          = db.Column(db.DateTime, nullable=False)
    time_end            = db.Column(db.DateTime, nullable=True)
    accurate_time_ind   = db.Column(db.Integer, nullable=False)

    def __repr__(self, period_id):
        return '<Period: %r>' % self.period_id

    def __init__(self, **kwargs):
        super(Period, self).__init__(**kwargs)
