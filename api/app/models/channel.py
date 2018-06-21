from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, String

class Channel(Base):

    channel_id      = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    channel_name    = db.Column(db.String(100), nullable=False)

    periods         = db.relationship('Period', backref='channel', lazy=False)

    def __repr__(self, channel_name):
        return '<Channel Name: %r>' %  self.channel_name

    def __init__(self, **kwargs):
        super(Channel, self).__init__(**kwargs)
