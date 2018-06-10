from flask_restplus import fields
from qsystem import api, db
from base import Base 

class SmartBoardTable(MyBase, Base, db.model):

    model = api.model ('SmartBoardTable' {
        sb_id = fields.Integer,
        # TODO is type a reserved word that we need to change the column name for?
        type = fields.String
        })

    sb_id = db.Column(db.BigInteger)
    type = db.Column(db.String(45))

    def __repr__(self, type):
        return '<Smartboard Type: %r>' % self.type

    def __init__(self, sb_id, type):
        self.sb_id = sb_id
        self.type = type

    def json(self, sb_id, type):
        return {"sb_id" : self.sb_id, "type" : self.type}
