from sqlalchemy import Column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, JSON
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())

class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(User.id), nullable=False)
    content = Column(String)
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())

class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True)
    members = Column(JSON)
    messages = Column(JSON)
    created_dtm = Column(DateTime(timezone=True), server_default=func.now())

class Notifier(Base):
    __tablename__ = "notifier"
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(User.id), nullable=False)
    room_id = Column(ForeignKey(Room.id), nullable=False)
    last_seen = Column(DateTime)
