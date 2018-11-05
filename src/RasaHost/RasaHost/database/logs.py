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
        offset = (page - 1) * pageCount
        like = "%" + query + "%"
        return self.session.query(Log) \
                        .filter(
                            Log.name.like(like) | \
                                Log.name.like(like) | \
                                Log.module.like(like) | \
                                Log.filename.like(like) | \
                                Log.log_level.like(like) | \
                                Log.exception.like(like) | \
                                Log.sender_id.like(like) | \
                                Log.request_id.like(like)  \
                            ) \
                        .order_by(Log.created.desc()) \
                        .limit(pageCount).offset(offset)
  
    def find_conversations(self, query, page, pageCount):
        offset = (page - 1) * pageCount
        like = "%" + query + "%"
        requests_ids = self.session.query(Log.request_id) \
                        .filter(Log.sender_id.isnot(None)) \
                        .filter(
                            Log.name.like(like) | \
                                Log.name.like(like) | \
                                Log.module.like(like) | \
                                Log.filename.like(like) | \
                                Log.log_level.like(like) | \
                                Log.exception.like(like) | \
                                Log.sender_id.like(like) | \
                                Log.request_id.like(like)  \
                            ) \
                        .group_by(Log.request_id) \
                        .order_by(Log.created.desc()) \
                        .limit(pageCount).offset(offset)

        return self.session.query(Log) \
            .filter(Log.request_id.in_(requests_ids))

    def save(self, log):
        self.session.add(log)
        pass
