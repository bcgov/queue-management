from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import Period
from qsystem import db

class PeriodSchema(ModelSchema):

    period_id           = fields.Int()
    sr_id               = fields.Int()
    csr_id              = fields.Int()
    reception_csr_ind   = fields.Int()
    channel_id          = fields.Int()
    ps_id               = fields.Int()
    time_start          = fields.DateTime()
    time_end            = fields.DateTime()
    accurate_time_ind   = fields.Integer()