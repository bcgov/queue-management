from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import PeriodState
from qsystem import db

class PeriodStateSchema(ModelSchema):

    ps_id           = fields.Int()
    ps_name         = fields.Str()
    ps_desc         = fields.Str()
    ps_number       = fields.Int()