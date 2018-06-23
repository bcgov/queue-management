from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import CSRState
from qsystem import db

class CSRStateSchema(ModelSchema):

    csr_state_id    = fields.Int()
    csr_state_name  = fields.Str()
    csr_state_desc  = fields.Str()