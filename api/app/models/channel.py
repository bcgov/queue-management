from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, String

class Channel(Base):

    model = api.model('Channel', {
        'channel_id': fields.Integer,
        'channel_name': fields.String
        })

    channel_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    channel_name    = db.Column(db.String(100))

    periods         = db.relationship('Period', backref='channel', lazy=False)

    def __repr__(self, channel_name):
        return '<Channel Name: %r>' %  self.channel_name

    def __init__(self, **kwargs):
        super(Channel, self).__init__(**kwargs)

    def __json__(self, channel_id, channel_name):
        return {"channel_id" : self.channel_id, 
                "channel_name" : self.channel_name}