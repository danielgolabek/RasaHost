import sqlalchemy
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#Base = declarative_base()
from RasaHost.database.metadata import Base

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    module = Column(String)
    filename = Column(String)
    line_no = Column(Integer)
    log_level = Column(String)
    message = Column(String)
    exception = Column(String)
    created = Column(DateTime)
    sender_id = Column(String)
    
class LogRepository:
    def __init__(self, session):
        self.session = session

    def find(self, query):
        return self.session.query(Log).all()

    def save(self, log):
        self.session.add(log)
        pass
