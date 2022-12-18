from app.api.crud.users import insert_user
from app.api.crud.rooms import insert_room, update_messages_in_room
from app.api.crud.messages import insert_message
from app.api.schemas.users import Login
from app.api.schemas.rooms import CreateRoom

USER_NAME = ['test1', 'test2']
MESSAGES = ['Halo', 'Apa kabar?']


def users(db):
    user_id = []
    for u in USER_NAME:
        data = Login(**{'name': u})
        user = insert_user(data, db)
        user_id.append(user.id)

    return user_id


def room(sender, receiver, db):
    data = CreateRoom(**{'sender': sender,
                         'receiver': receiver})

    return insert_room(data, db)


def messages(room, db):
    sender_id = 1

    for m in MESSAGES:
        msg = insert_message(user_id=sender_id, content=m, db=db)
        update_messages_in_room(id=room.id, message_id=msg.id, db=db)
