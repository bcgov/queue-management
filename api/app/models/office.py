from flask_restplus import fields
from qsystem import api, db

class Office(db.Model):
    __tablename__ = 'offices'

    model = api.model('Office', {
        'id': fields.String,
        'name': fields.String
    })

    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name    = db.Column(db.String(80), nullable=False)
    clients = db.relationship("Client")
    users   = db.relationship("User", back_populates="office")

    def __repr__(self):
        return '<Office %r>' % self.name

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"name": self.name}
