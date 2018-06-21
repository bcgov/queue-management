from flask_restplus import fields
from qsystem import api, db
from .base import Base 
#from app.models import Role
from sqlalchemy import BigInteger, String

class Permission(Base):

    permission_id    = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    permission_code  = db.Column(db.String(100), nullable=False)
    permission_desc  = db.Column(db.String(1000), nullable=False)

    #roles        = db.relationship("Role", secondary=Role.role_right, back_populates="rights")

    def __repr__(self, permission_code):
        return '<Permission Code: %r>' % self.permission_code

    def __init__(self, **kwargs):
        super(Permission, self).__init__(**kwargs)
