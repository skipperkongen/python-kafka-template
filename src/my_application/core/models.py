from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Action(Base):
    __tablename__ = 'actions'
    # __table_args__ = {'schema' : 'pkt'}    
    id = Column(Integer, primary_key=True)
    subject = Column(String)
    action = Column(String)

    def __repr__(self):
        return "<Action(id='%s')>" % (self.id)

    def serialize(self):
        return {"id": self.id,
                "subject": self.subject,
                "action": self.action}
