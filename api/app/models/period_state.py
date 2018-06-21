from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, Integer, String

# TODO Please review the valid state table to see for testing
class PeriodState(Base):

    ps_id           = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    ps_name         = db.Column(db.String(100), nullable=False)
    ps_desc         = db.Column(db.String(1000), nullable=False)
    ps_number       = db.Column(db.Integer, nullable=False)

    periods         = db.relationship('Period', backref='period_state', lazy=False)

    def __repr__(self, ps_name):
        return '<Period State Name: %r>' % self.ps_name

    def __init__(self, **kwargs):
        super(PeriodState, self).__init__(**kwargs)
