from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class ChannelSchema(ModelSchema):

    channel_id      = fields.Int(dump_only=True)
    channel_name    = fields.Str()