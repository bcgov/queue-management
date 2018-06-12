from flask_restplus import fields
from qsystem import api, db
from base import Base 

class PeriodTable (MyBase, Base, db.model):

    model = api.model('PeriodTable' {
            'period_id' : fields.Integer,
            'sr_id' : fields.Integer,
            'csr_id' : fields.Integer,
            'reception_csr' : fields.Integer,
            'channel_id' : fields.Integer,
            'ps_id' : fields.Integer,
            # TODO see if datetime object exists for time_start and time_end
            'time_start' : fields.String,
            'time_end' : fields.String,
            'accurate_time' : fields.Integer
        })

    period_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    # TODO possible FK for sr_id
    sr_id = db.Column(db.BigInteger)
    # TODO possible FK for csr_id
    csr_id = db.Column(db.BigInteger)
    # TODO find better datatype for tinyint(1) for reception_csr
    reception_csr = db.Column(Integer)
    # TODO possible FK for channel_id
    channel_id = db.Column(db.BigInteger)
    # TODO possible FK for ps_id
    ps_id = db.Column(db.BigInteger)
    time_start = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    # TODO find better dataype for tinyint(1) for accurate_time
    accurate_time = db.Column(db.Integer)

    def __repr__(self, period_id):
        return '<Period: %r>' % self.period_id

    def __init__(self, period_id, sr_id, csr_id, reception_csr, channel_id, ps_id, time_start, time_end, accurate_time):
        self.period_id = period_id
        self.sr_id = sr_id
        self.csr_id = csr_id
        self.reception_csr = reception_csr
        self.channel_id = channel_id
        self.ps_id = ps_id
        self.time_start = time_start    
        self.time_end = time_end
        self.accurate_time = accurate_time

    def json(self, period_id, sr_id, csr_id, reception_csr, channel_id, ps_id, time_start, time_end, accurate_time):
        return {"period_id" : self.period_id, "sr_id" : self.sr_id, "csr_id" : self.csr_id, 
                "reception_csr" : self.reception_csr, "channel_id" : self.channel_id, "ps_id" : self.ps_id, 
                "time_start" : self.time_start, "time_end" : self.time_end, "accurate_time" : self.accurate_time} 