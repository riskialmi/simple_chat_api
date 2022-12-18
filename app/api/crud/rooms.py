from sqlalchemy.orm import Session
from sqlalchemy import text, and_, func
from datetime import datetime

from app.db import models


def insert_room(param, db: Session):
    room = models.Room(members=[param.sender, param.receiver])
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


def get_room_by_members(param, db: Session):
    return db.query(models.Room) \
        .filter(and_(func.jsonb(models.Room.members).op("@>")(str(param.sender)),
                     func.jsonb(models.Room.members).op("@>")(str(param.receiver)))) \
        .first()


def get_rooms_by_user_id(user_id, db: Session):
    return db.query(models.Room).filter(text(f''' members::jsonb @> '{user_id}' ''')).all()


def query_room_by_id(id, db: Session):
    return db.query(models.Room).filter_by(id=id)


def update_messages_in_room(id, message_id, db: Session):
    room = query_room_by_id(id, db)
    messages = room.first().messages

    if messages:
        messages.append(message_id)
    else:
        messages = [message_id]

    room.update({'messages': messages})
    db.commit()


def get_notifier(room_id, user_id, db: Session):
    return db.query(models.Notifier) \
        .filter(and_(models.Notifier.room_id == room_id, models.Notifier.user_id == user_id)) \
        .first()


def insert_notifier(room_id, user_id, last_seen, db: Session):
    notifier = models.Notifier(room_id=room_id, user_id=user_id, last_seen=last_seen)
    db.add(notifier)
    db.commit()
    db.refresh(notifier)
    return notifier


def update_notifier(room_id, user_id, last_seen, db: Session):
    notifier = db.query(models.Notifier) \
        .filter(and_(models.Notifier.room_id == room_id, models.Notifier.user_id == user_id))
    notifier.update({'last_seen': last_seen})
    db.commit()
    return notifier
