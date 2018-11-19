import sqlalchemy
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#Base = declarative_base()
from RasaHost.database.metadata import Base

class Conversation(Base):
    __tablename__ = 'conversation'
    id = Column(Integer, primary_key=True)
    request = Column(String)
    response = Column(String)
    created = Column(DateTime)
    sender_id = Column(String)
    request_id = Column(String)
    
class ConversationRepository:
    def __init__(self, session):
        self.session = session

    def find(self, query, page, pageCount):
        offset = (page - 1) * pageCount
        like = "%" + query + "%"
        return self.session.query(Conversation) \
                        .filter(
                                Conversation.request.like(like) | \
                                Conversation.response.like(like) | \
                                Conversation.sender_id.like(like) | \
                                Conversation.request_id.like(like)  \
                            ) \
                        .order_by(Conversation.created.desc()) \
                        .limit(pageCount).offset(offset)
  
    def save(self, conversation):
        self.session.add(conversation)
        pass
