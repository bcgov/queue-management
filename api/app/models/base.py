from flask_restplus import fields
from qsystem import api, db

class Base(object):

	@declared_attr
	def __tablename__(cls):
		return cls.__name__.lower()