import os

from sqlalchemy import create_engine

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

#engine = create_engine('sqlite:////tmp/test.db')
engine = create_engine('postgresql://postgres:password@db:5432/postgres')

Session = scoped_session(sessionmaker(bind=engine))
