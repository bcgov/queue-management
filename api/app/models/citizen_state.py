from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, String

class CitizenState(Base):

    cs_id           = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    cs_state_name   = db.Column(db.String(100), nullable=False)
    cs_state_desc   = db.Column(db.String(1000), nullable=False)

    citizens        = db.relationship('Citizen', backref='citizen_state', lazy=False)

    def __repr__(self, cs_state_name):
        return '<CS State Name: %r>' % self.cs_state_name

    def __init__(self, **kwargs):
        super(CitizenState, self).__init__(**kwargs)
