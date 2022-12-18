from sqlalchemy.orm import Session
from datetime import datetime

from app.api.crud.messages import get_messages_by_ids
from app.api.crud.rooms import get_room_by_members, insert_room, update_messages_in_room, get_notifier, \
    insert_notifier, update_notifier, get_rooms_by_user_id
from app.api.crud.messages import insert_message, get_conversations


def create_room(param, db: Session):
    room = get_room_by_members(param, db)

    if not room:
        room = insert_room(param, db)

    data = room.__dict__
    data.update(param)
    data['messages'] = get_messages_by_ids(room.messages, db)
    return data

async def upload_message_to_room(data, db: Session):
    message = insert_message(user_id=data['user_id'], content=data['content'], db=db)
    update_messages_in_room(id=data['room_id'], message_id=message.id, db=db)

def update_last_seen(room_id, user_id, db: Session):
    notifier = get_notifier(room_id, user_id, db)
    last_seen = datetime.now()

    if not notifier:
        return insert_notifier(room_id, user_id, last_seen, db)

    return update_notifier(room_id, user_id, last_seen, db)

def get_all_conversations_with_user(user_id, db: Session):
    conversations = []
    rooms = get_rooms_by_user_id(user_id, db)
    for room in rooms:
        conversations.append(get_conversations(user_id, room.members, room.messages, db))

    return conversations
