from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db import models

def insert_user(param, db: Session):
    user = models.User(name=param.name)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_name(name, db: Session):
    return db.query(models.User).filter_by(name=name).first()


def get_users(db):
    users = db.query(models.User).all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return users
