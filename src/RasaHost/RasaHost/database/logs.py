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
    request_id = Column(String)
    
class LogRepository:
    def __init__(self, session):
        self.session = session

    def find(self, query, page, pageCount):
        
        findLogs = self.session.query(Log)

        for part in query:
            if isinstance(part, dict):
                key = next(iter(part.keys()))
                value = part[key]
                findLogs = findLogs.filter(self.like(key, value))
            else:
                findLogs = findLogs.filter(self.like(None, str(part)))

        return findLogs \
            .order_by(Log.created.desc()) \
            .limit(pageCount).offset((page - 1) * pageCount)
  
    def find_rasa(self, query, page, pageCount):

        requests_ids = self.session.query(Log.request_id).filter(Log.sender_id.isnot(None))

        for part in query:
             if isinstance(part, dict):
                 key = next(iter(part.keys()))
                 value = part[key]
                 requests_ids = requests_ids.filter(self.like(key, value))
             else:
                 requests_ids = requests_ids.filter(self.like(None, str(part)))

        requests_ids = requests_ids.group_by(Log.request_id) \
            .order_by(Log.created.desc()) \
            .limit(pageCount).offset((page - 1) * pageCount)

        return self.session.query(Log) \
            .filter(Log.request_id.in_(requests_ids)) \
            .order_by(Log.created.desc())

    def like(self, name, value):
        like = "%" + value + "%"
        if name == "message":
            return Log.message.like(like) | Log.exception.like(like)
        if name == "module":
            return Log.module.like(like)
        if name == "sender":
            return Log.sender_id.like(like)
        if name == "request":
            return Log.request_id.like(like)
        return Log.name.like(like) | \
            Log.name.like(like) | \
            Log.module.like(like) | \
            Log.filename.like(like) | \
            Log.log_level.like(like) | \
            Log.message.like(like) | \
            Log.exception.like(like) | \
            Log.sender_id.like(like) | \
            Log.request_id.like(like)  \
    

    def save(self, log):
        self.session.add(log)
        pass
