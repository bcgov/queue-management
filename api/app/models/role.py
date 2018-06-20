from flask_restplus import fields
from qsystem import api, db
from .base import Base 
#
from app.models import Right
from sqlalchemy import BigInteger, String

class Role(Base):

    role_right  = db.Table('role_right',
                            db.Column('role_id', db.Integer, 
                                      db.ForeignKey('role.role_id'), primary_key=True),
                            db.Column('right_id', db.Integer,
                                      db.ForeignKey('right.right_id'), primary_key=True)
    )

    model = api.model('Role', {
    'role_id': fields.Integer,
    'role_code': fields.String,
    'role_desc': fields.String
    })

    role_id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_code   = db.Column(db.String(100))
    role_desc   = db.Column(db.String(1000))

    roles       = db.relationship('CSR', backref='role', lazy=False)
    rights      = db.relationship("Right", secondary=role_right, back_populates="roles")


    def __repr__(self, role_code):
        return '<Role Code: %r>' % self.role_code

    def __init__(self, role_code, role_desc):
        self.role_code  = role_code
        self.role_desc  = role_desc

    def json(self, role_id, role_code, role_desc):
        return {"role_id" : self.role_id, 
        "role_code" : self.role_code, 
        "role_desc" : self.role_desc}