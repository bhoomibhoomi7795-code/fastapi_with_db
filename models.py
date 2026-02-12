from db import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    password = Column(String)

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    ai_response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)




