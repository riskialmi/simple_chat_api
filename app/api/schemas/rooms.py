from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.api.schemas.users import UserRoom


class Message(BaseModel):
    id: int
    user_id: int
    content: str
    created_dtm: datetime

    class Config:
        orm_mode = True

class Room(UserRoom):
    id: int
    messages: List[Message]

    class Config:
        orm_mode = True

class Conversation(BaseModel):
    last_message: str
    user_name: str
    unread_count: int

