from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import SRState
from qsystem import db

class SRStateSchema(ModelSchema):

    sr_state_id     = fields.Int()
    sr_code         = fields.Str()
    sr_state_desc   = fields.Str()
