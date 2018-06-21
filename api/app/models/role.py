from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from app.models import Permission
from sqlalchemy import BigInteger, String

class Role(Base):

    role_permission     = db.Table('role_permission',
                                    db.Column('role_id', db.Integer, 
                                            db.ForeignKey('role.role_id'), primary_key=True, nullable=False),
                                    db.Column('permission_id', db.Integer,
                                            db.ForeignKey('permission.permission_id'), primary_key=True, nullable=False)
    )

    role_id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_code   = db.Column(db.String(100))
    role_desc   = db.Column(db.String(1000))

    roles       = db.relationship('CSR', backref='role', lazy=False)
    #rights      = db.relationship("Right", secondary=role_right, back_populates="roles")

    def __repr__(self, role_code):
        return '<Role Code: %r>' % self.role_code

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
