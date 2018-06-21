from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, String

class SmartBoard(Base):

    model = api.model ('SmartBoard', {
        'sb_id': fields.Integer,
        'type': fields.String
        })

    sb_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type    = db.Column(db.String(45))

    def __repr__(self, type):
        return '<Smartboard Type: %r>' % self.type

    def __init__(self, **kwargs):
        super(SmartBoard, self).__init__(**kwargs)

    def json(self, sb_id, type):
        return {"sb_id" : self.sb_id, 
                "type" : self.type}
