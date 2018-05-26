from qsystem import db

class Note(db.Model):
    __tablename__ = 'notes'

    id    = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(1000))

    def __init__(self, value):
        self.value = value

    def json(self):
        return {"value": self.value}
