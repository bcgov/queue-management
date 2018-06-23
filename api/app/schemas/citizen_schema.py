from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import Citizen
from qsystem import db

class CitizenSchema(ModelSchema):

    class Meta:
        model = Citizen
        sqla_session = db.session

    citizen_id          = fields.Int(dump_only=True)
    office_id           = fields.Int()
    ticket_number       = fields.Str(dump_only=True)
    citizen_name        = fields.Str()
    citizen_comments    = fields.Str()
    qt_xn_citizen_ind   = fields.Int()
    cs_id               = fields.Int()
    start_time          = fields.DateTime(dump_only=True)