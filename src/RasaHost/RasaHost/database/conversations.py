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
    response_raw = Column(String)
    created = Column(DateTime)
    sender_id = Column(String)
    request_id = Column(String)
    
    
class ConversationRepository:
    def __init__(self, session):
        self.session = session

    def find(self, query, page, pageCount):
        
        findConvers  = self.session.query(Conversation) 
        
        for part in query:
            if isinstance(part, dict):
                key = next(iter(part.keys()))
                value = part[key]
                findConvers = findConvers.filter(self.like(key, value))
            else:
                findConvers = findConvers.filter(self.like(None, str(part)))

        return findConvers \
                .order_by(Conversation.created.desc()) \
                .limit(pageCount).offset((page - 1) * pageCount)
  
    def like(self, name, value):
        like = "%" + value + "%"
        if name == "message":
            return Conversation.request.like(like) | Conversation.response.like(like)
        if name == "sender":
            return Conversation.sender_id.like(like)
        if name == "request":
            return Conversation.request_id.like(like)
        return Conversation.request.like(like) | \
            Conversation.response.like(like) | \
            Conversation.sender_id.like(like) | \
            Conversation.request_id.like(like)  \

    def save(self, conversation):
        self.session.add(conversation)
        pass
