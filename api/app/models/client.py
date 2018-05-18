from flask_restplus import fields
from qsystem import api, db

class Client(db.Model):
    __tablename__ = 'clients'

    model = api.model('Office', {
        'id': fields.String,
        'name': fields.String,
        'office_id': fields.String
    })

    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name      = db.Column(db.String(80), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('offices.id'))

    def __repr__(self):
        return '<Client %r>' % self.name

    def __init__(self, name, office_id):
        self.name = name
        self.office_id = office_id

    def json(self):
        return {"name": self.name, "office_id": self.office_id}
