from flask_restplus import fields
from qsystem import api, db
from .base import Base 
from sqlalchemy import BigInteger, Integer, DateTime

class Period(Base):

    model = api.model('Period', {
            'period_id' : fields.Integer,
            'sr_id' : fields.Integer,
            'csr_id' : fields.Integer,
            'reception_csr' : fields.Integer,
            'channel_id' : fields.Integer,
            'ps_id' : fields.Integer,
            'time_start' : fields.String,
            'time_end' : fields.String,
            'accurate_time' : fields.Integer
        })

    period_id       = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    sr_id           = db.Column(db.BigInteger, db.ForeignKey('service_req.sr_id'))
    csr_id          = db.Column(db.BigInteger, db.ForeignKey('csr.csr_id'))
    reception_csr   = db.Column(Integer)
    channel_id      = db.Column(db.BigInteger, db.ForeignKey('channel.channel_id'))
    ps_id           = db.Column(db.BigInteger, db.ForeignKey('period_state.ps_id'))
    time_start      = db.Column(db.DateTime)
    time_end        = db.Column(db.DateTime)
    accurate_time   = db.Column(db.Integer)

    sr = db.relationship("Service_req")
    csr = db.relationship("CSR")
    channel = db.relationship("Channel")
    ps = db.relationship("PS")

    def __repr__(self, period_id):
        return '<Period: %r>' % self.period_id

    args = {'period_id': 'period_id',
            'sr_id': 'sr_id',
            'csr_id': 'csr_id',
            'reception_csr': 'reception_csr',
            'channel_id': 'channel_id',
            'ps_id': 'ps_id',
            'time_start': 'time_start',
            'time_end': 'time_end',
            'accurate_time': 'accurate_time'}

    def __init__(self, **args):
        self.period_id      = args['period_id']
        self.sr_id          = args['sr_id']
        self.csr_id         = args['csr_id']
        self.reception_csr  = args['reception_csr']
        self.channel_id     = args['channel_id']
        self.ps_id          = args['ps_id']
        self.time_start     = args['time_start']    
        self.time_end       = args['time_end']
        self.accurate_time  = args['accurate_time']

    json_args = {'period_id': "period_id", 
                'sr_id': "sr_id", 
                'csr_id': "csr_id", 
                'reception_csr' : "reception_csr", 
                'channel_id' : "channel_id", 
                'ps_id' : "ps_id", 
                'time_start' : "time_start", 
                'time_end' : "time_end", 
                'accurate_time' : "accurate_time"} 

    def json(self, **json_args):
        return {json_args['period_id']: self.period_id,
                json_args['sr_id']: self.sr_id,
                json_args['csr_id']: self.csr_id,
                json_args['reception_csr']: self.reception_csr,
                json_args['channel_id']: self.channel_id,
                json_args['ps_id']: self.ps_id,
                json_args['time_start']: self.time_start,
                json_args['time_end']: self.time_end,
                json_args['accurate_time']: self.accurate_time}