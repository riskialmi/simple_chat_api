from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Json, ValidationError, validator, create_model, EmailStr, constr
from datetime import date, datetime


class CreateRoom(BaseModel):
    sender: int
    receiver: int

class Message(BaseModel):
    id: int
    user_id: int
    content: str
    created_dtm: datetime

    class Config:
        orm_mode = True

class Room(CreateRoom):
    id: int
    messages: List[Message]

    class Config:
        orm_mode = True

class Conversation(BaseModel):
    last_message: str
    user_name: str
    unread_count: int

