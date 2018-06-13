from flask_restplus import fields
from qsystem import api, db
from .base import Base 

class RoleRight(Base):

    model = api.model('RoleRight', {
        'role_id' : fields.Integer,
        'right_id' : fields.Integer
        })

    role_id     = db.Column(db.BigInteger)
    right_id    = db.Column(db.BigInteger)

    # TODO do we need repr for testing?

    def __init__(self, role_id, right_id):
        self.role_id    = role_id
        self.right_id   = right_id

    def json (self, role_id, right_id):
        return {"role_id" : self.role_id, 
                "right_id" : self.right_id}