from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String)
    action = db.Column(db.String)

    def __init__(self, subject, action):
        self.subject = subject
        self.action = action

    def serialize(self):
        return {"id": self.id,
                "subject": self.subject,
                "action": self.action}
