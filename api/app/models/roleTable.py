from flask_restplus import fields
from qsystem import api, db
from base import Base 

class RoleTable(MyBase, Base, db.model):

     model = api.model('RoleTable' {
        'role_id' : fields.Integer,
        'role_code' : fields.String,
        'role_desc' : fields.String
        })

     role_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
     role_code = db.Column(db.String(100))
     role_desc = db.Column(db.String(1000))

     def __repr__(self, role_code):
        return '<Role Code: %r>' % self.role_code

    def __init__(self, role_id, role_code, role_desc):
        self.role_id = role_id
        self.role_code = role_code
        self.role_desc = role_desc

    def json(self, role_id, role_code, role_desc):
        return {"role_id" : self.role_id, "role_code" : self.role_code, "role_desc" : self.role_desc}