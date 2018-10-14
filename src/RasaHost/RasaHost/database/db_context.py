import sqlalchemy
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#Base = declarative_base()
from RasaHost.database.logs import Log, LogRepository
from RasaHost.database.metadata import Base

class DbContext(object):
    def __init__(self):
        self.dbEngine = create_engine('sqlite:///db.sqlite')
        self.dbSession = sessionmaker()
        self.dbSession.configure(bind=self.dbEngine)
        Base.metadata.create_all(self.dbEngine)
        self.session = self.dbSession()
        
        self.logs = LogRepository(self.session)

    def commit(self):
        self.session.commit()


