from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, String

class SmartBoard(Base):

    sb_id       = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    sb_type     = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return '<Smartboard Type:(name={self.sb_type!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(SmartBoard, self).__init__(**kwargs)
