from typing import List, Union
from fastapi import APIRouter, Depends, WebSocket

import app.api.schemas.users
from app.api.schemas import rooms as schemas
from app.api.schemas import users
from app.db.database import get_db
from app.controllers.rooms import *


router = APIRouter(tags=["Rooms"])

@router.post("/room", response_model=schemas.Room)
async def room(param: users.UserRoom, db: Session = Depends(get_db)):
    return create_room(param, db)

@router.get("/room/conversation/{user_id}", response_model=List[schemas.Conversation])
async def get_conversation(user_id: int, db: Session = Depends(get_db)):
    return get_all_conversations_with_user(user_id, db)
