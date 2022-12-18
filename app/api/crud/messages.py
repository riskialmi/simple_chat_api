from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, and_, or_, text, asc

from app.db import models


def get_messages_by_ids(ids, db: Session):
    return db.query(models.Message).filter_by(id=func.any(ids)).all()

def get_message_by_id(id, db: Session):
    return db.query(models.Message).filter_by(id=id).first()

def insert_message(user_id, content, db: Session):
    message = models.Message(user_id=user_id, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_conversations(user_id, members, messages, db: Session):
    message_1 = aliased(models.Message)
    message_2 = aliased(models.Message)
    last_msg_id = max(messages)

    return db.query(models.User.name.label('user_name'),
                    func.count(message_1.id).label('unread_count'),
                    message_2.content.label('last_message')
                    )\
        .select_from(models.User)\
        .join(message_1, message_1.id == func.any(messages))\
        .join(message_2, message_2.id == last_msg_id)\
        .join(models.Notifier, models.Notifier.last_seen < message_1.created_dtm)\
        .filter(and_(models.User.id != user_id, models.User.id == func.any(members)))\
        .group_by(models.User.name, message_2.id)\
        .first()

