from flask_restplus import fields
from qsystem import api, db
from base import Base 

class CSR(Base):

    model = api.model ('CSR' {
        'csr_id' : fields.Integer,
        'username' : fields.String,
        'password' : fields.String,
        'office_id_in_now' : fields.Integer,
        'role_id' : fields.String,
        'qt_xn_csr_now' : fields.Integer,
        'receptionist_now' : fields.Integer,
        'deleted' : fields.String,
        'csr_state_id_now' : fields.Integer
    })

    csr_id              = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username            = db.Column(db.String(150))
    password            = db.Column(db.String(45), nullable=False)
    # TODO check FK for Office Table
    office_id_in_now    = db.Column(db.BigInteger)
    # TODO check FK for Role Table
    role_id             = db.Column(db.BigInteger)
    qt_xn_csr_now       = db.Column(db.Binary)
    receptionist_now    = db.Column(db.Integer)
    deleted             = db.Column(db.DateTime, nullable=True)
    csr_state_id_now    = db.Column(db.BigInteger)

    def __repr__(self, username):
        return '<CSR User: %r>' % self.username

    # TODO redo init function to include kwargs
    def __init__(self, csr_id, username, password, office_id_in_now, role_id, qt_xn_csr_now, 
                receptionist_now, deleted, csr_state_id_now):
        self.csr_id             = csr_id
        self.username           = username
        self.password           = password
        self.office_id_in_now   = office_id_in_now
        self.role_id            = role_id
        self.qt_xn_csr_now      = qt_xn_csr_now
        self.receptionist_now   = receptionist_now
        self.deleted            = deleted
        self.csr_state_id_now   = csr_state_id_now

    # TODO Check normal line length for large return values 
    def json(self, csr_id, username, password, office_id_in_now, role_id, qt_xn_csr_now, 
            receptionist_now, deleted, csr_state_id_now):
        return {"csr_id" : self.csr_id, 
                "username" : self.username, 
                "password" : self.password, 
                "office_id_in_now" : office_id_in_now, 
                "role_id" : self.role_id, 
                "qt_xn_csr_now" : self.qt_xn_csr_now, 
                "receptionist_now" : self.receptionist_now, 
                "deleted" : self.deleted, 
                "csr_state_id_now" : self.csr_state_id_now}