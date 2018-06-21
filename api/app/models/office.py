d           = db.Column(db.Integer, db.ForeignKey('smartboard.sb_id'), nullable=False)
    deleted         = db.Column(db.DateTime, nullable=True)

    services        = db.relationship("Service", secondary=office_service, back_populates="offices")
    offices         = db.relationship('CSR', backref='office', lazy=False)
    citizens        = db.relationship('Citizen', backref='office', lazy=False)

    def __repr__(self, office_name):
        return '<Office: %r>' % self.office_name

    def __init__(self, **kwargs):
        super(Office, self).__init__(**kwargs)
