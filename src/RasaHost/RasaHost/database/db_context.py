import sqlalchemy
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
#Base = declarative_base()
from RasaHost.database.logs import Log, LogRepository
from RasaHost.database.conversations import Conversation, ConversationRepository
from RasaHost.database.metadata import Base

class DbContext(object):
    dbEngine = create_engine('sqlite:///rasa-host.sqlite')
    Base.metadata.create_all(dbEngine)
    dbSessionFactory = scoped_session(sessionmaker(bind=dbEngine))

    def __init__(self):
        self.session = self.dbSessionFactory()
        self.logs = LogRepository(self.session)
        self.conversations = ConversationRepository(self.session)

    def commit(self):
        self.session.commit()


