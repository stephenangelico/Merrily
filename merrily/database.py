import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from flask_login import UserMixin

from merrily import app

engine = create_engine(app.config["DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class RingEvent(Base):
	__tablename__ = "ringevents"
	
	id = Column(Integer, primary_key=True)
	timestamp = Column(DateTime, default=datetime.datetime.now)
	entity = Column(String(128))
	notes = Column(String(1024))
	answered = Column(Boolean, default=False)

class User(Base, UserMixin):
	__tablename__ = "users"
	
	id = Column(Integer, primary_key=True)
	name = Column(String(128))
	email = Column(String(128), unique=True)
	password = Column(String(128))
