from flask_restplus import fields
from qsystem import api, db

class User(db.Model):
    __tablename__ = 'users'

    model = api.model('User', {
        'id': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'username': fields.String,
        'office_id': fields.String,
        'office.name': fields.String
    })

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name =db.Column(db.String(80), nullable=True)
    last_name  = db.Column(db.String(80), nullable=True)
    username   = db.Column(db.String(80), nullable=False)
    office_id  = db.Column(db.Integer, db.ForeignKey('offices.id'))
    office     = db.relationship("Office", back_populates="users")

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, username, office_id):
        self.username = username
        self.office_id = office_id

    def json(self):
        return {"name": self.name, "office_id": self.office_id}