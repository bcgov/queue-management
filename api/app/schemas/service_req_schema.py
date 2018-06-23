from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app.models import ServiceReq
from qsystem import db

class ServiceReqSchema(ModelSchema):

    sr_id       = fields.Int()
    citizen_id  = fields.Int()
    quantity    = fields.Int()
    service_id  = fields.Int()
    sr_state_id = fields.Int()