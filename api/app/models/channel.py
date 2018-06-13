from flask_restplus import fields
from qsystem import api, db
from .base import Base 

class Channel(Base):

    model = api.model('Channel', {
        'channel_id' : fields.Integer,
        'channel_name' : fields.String
        })

    channel_id      = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    channel_name    = db.Column(db.String(100))

    def __repr__(self, channel_name):
        return '<Channel Name: %r>' %  self.channel_name

    def __init__(self, channel_id, channel_name):
        self.channel_id     = channel_id
        self.channel_name   = channel_name

    def __json__(self, channel_id, channel_name):
        return {"channel_id" : self.channel_id, 
                "channel_name" : self.channel_name}