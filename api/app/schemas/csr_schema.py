from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import CSR
from qsystem import db

class CSRSchema(ModelSchema):

    csr_id              = fields.Int()
    username            = fields.Str()
    office_id           = fields.Int()
    role_id             = fields.Int()
    qt_xn_csr_ind       = fields.Int()
    receptionist_ind    = fields.Int()
    deleted             = fields.DateTime()
    csr_state_id        = fields.Int()
