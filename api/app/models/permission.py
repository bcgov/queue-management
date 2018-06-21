from flask_restplus import fields
from qsystem import api, db
from .base import Base 
#from app.models import Role
from sqlalchemy import BigInteger, String

class Permission(Base):

    model = api.model('Permission', {
        'permission_id': fields.Integer,
        'permission_code': fields.String,
        'permission_desc': fields.String
        })

    permission_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    permission_code  = db.Column(db.String(100))
    permission_desc  = db.Column(db.String(1000))

    #roles        = db.relationship("Role", secondary=Role.role_right, back_populates="rights")

    def __repr__(self, permission_code):
        return '<Permission Code: %r>' % self.permission_code

    def __init__(self, **kwargs):
        super(Permission, self).__init__(**kwargs)

    def json(self, permission_id, permission_code, permission_desc):
        return {"permission_id" : self.permission_id, 
                "permission_code" : self.permission_code, 
                "permission_desc" : self.permission_desc}