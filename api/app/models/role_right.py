from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger

role_right  = db.Table('RoleRight',
                        db.Column('role_id', db.BigInteger, 
                                  db.ForeignKey('role.role_id'), primary_key=True),
                        db.Column('right_id', db.BigInteger,
                                  db.ForeignKey('right.right_id'), primary_key=True)
)

class RoleRight(Base):

    model = api.model('RoleRight', {
        'role_id' : fields.Integer,
        'right_id' : fields.Integer
        })

    role_id     = db.Column(db.BigInteger, primary_key=True)
    right_id    = db.Column(db.BigInteger, primary_key=True)

    def __init__(self, role_id, right_id):
        self.role_id    = role_id
        self.right_id   = right_id

    def json (self, role_id, right_id):
        return {"role_id" : self.role_id, 
                "right_id" : self.right_id}