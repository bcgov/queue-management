d           = db.Column(db.Integer, db.ForeignKey('smartboard.sb_id'), nullable=False)
    deleted         = db.Column(db.DateTime, nullable=True)

    services        = db.relationship("Service", secondary=office_service, back_populates="offices")
    csrs            = db.relationship('CSR', backref='office', lazy='joined')
    citizens        = db.relationship('Citizen', backref='office', lazy='joined')

    def __repr__(self):
        return '<Office Name:(name={self.office_name!r})>'.format(self=self)

    def __init__(self, **kwargs):
        super(Office, self).__init__(**kwargs)
