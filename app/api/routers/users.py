from typing import List
from fastapi import APIRouter, Depends

from app.api.schemas import users as schemas
from app.db.database import get_db
from app.api.crud import users
from app.controllers.users import *


router = APIRouter(tags=["Users"])

@router.post("/user/login", response_model=schemas.User)
async def login(param: schemas.Login, db: Session = Depends(get_db)):
    return get_user(param, db)

@router.get("/users", response_model=List[schemas.User])
async def get_users(db: Session = Depends(get_db)):
    return users.get_users(db)

