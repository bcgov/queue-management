from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, Integer, String, Binary, DateTime

class CSR(Base):

    model = api.model ('CSR', {
        'csr_id': fields.Integer,
        'username': fields.String,
        'password': fields.String,
        'office_id_in_now': fields.Integer,
        'role_id': fields.String,
        'qt_xn_csr_now': fields.Integer,
        'receptionist_now': fields.Integer,
        'deleted': fields.String,
        'csr_state_id': fields.Integer
    })

    csr_id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username            = db.Column(db.String(150))
    # Possibly Remove password column
    password            = db.Column(db.String(45), nullable=False)
    office_id           = db.Column(db.Integer, db.ForeignKey('office.office_id'))
    role_id             = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    qt_xn_csr_now       = db.Column(db.Binary)
    receptionist_now    = db.Column(db.Integer)
    deleted             = db.Column(db.DateTime, nullable=True)
    csr_state_id        = db.Column(db.Integer, db.ForeignKey('csrstate.csr_state_id'))

    periods             = db.relationship('Period', backref='csr', lazy=False)

    def __repr__(self, username):
        return '<CSR User: %r>' % self.username

    def __init__(self, **kwargs):
        super(CSR, self).__init__(**kwargs)

    def json(self, **json_args):
        return {json_args['csr_id']: self.csr_id,
                json_args['username']: self.username,
                json_args['password']: self.password,
                json_args['office_id_in_now']: self.office_id_in_now,
                json_args['role_id']: self.role_id,
                json_args['qt_xn_csr_now']: self.qt_xn_csr_now,
                json_args['receptionist_now']: self.receptionist_now,
                json_args['deleted']: self.deleted,
                json_args['csr_state_id_now']: self.csr_state_id_now}