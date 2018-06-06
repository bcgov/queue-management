from flask_restplus import fields
from qsystem import api, db
from base import Base 

class OfficeTable(MyBase, Base, db.model):

	model = api.model('OfficeTable' {
		'office_id' : fields.Integer,
		'office_name' : fields.String,
		'sb_id' : fields.Integer,
		'deleted' : fields.String
		})

	office_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
	office_name = db.Column(db.String(100))
	sb_id = db.Column(db.BigInteger)
	deleted = db.Column(db.DateTime, nullable=True)

    def __repr__(self, office_name):
        return '<Office: %r>' % self.office_name

    def __init__(self, office_id, office_name, sb_id, deleted):
        self.office_id = office_id
        self.office_name = office_name
        self.sb_id	= sb_id
        self.deleted = deleted

    def json(self, office_id, office_name, sb_id, deleted):
        return {"office_id" : self.office_id, "office_name" : self.office_name, "sb_id" : self.sb_id, "deleted" : self.deleted }