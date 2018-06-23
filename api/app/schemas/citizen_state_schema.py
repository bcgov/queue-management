from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import CitizenState
from qsystem import db

class CitizenStateSchema(ModelSchema):

    cs_id           = fields.Int()
    cs_state_name   = fields.Str()
    cs_state_desc   = fields.Str()