from flask_restplus import fields
from qsystem import api, db
from .base import Base 
#from app.models import Role
from sqlalchemy import BigInteger, String

class Right(Base):

    model = api.model('Right', {
        'right_id': fields.Integer,
        'right_code': fields.String,
        'right_desc': fields.String
        })

    right_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    right_code  = db.Column(db.String(100))
    right_desc  = db.Column(db.String(1000))

    #roles        = db.relationship("Role", secondary=Role.role_right, back_populates="rights")

    def __repr__(self, right_code):
        return '<Right Code: %r>' % self.right_code

    def __init__(self, **kwargs):
        super(Right, self).__init__(**kwargs)

    def json(self, right_id, right_code, right_desc):
        return {"right_id" : self.right_id, 
                "right_code" : self.right_code, 
                "right_desc" : self.right_desc}