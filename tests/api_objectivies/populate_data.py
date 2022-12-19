from app.api.crud.users import insert_user
from app.api.crud.rooms import insert_room, update_messages_in_room
from app.api.crud.messages import insert_message
from app.api.schemas.users import Login, UserRoom

# initial data
USER_NAME = {'sender': 'test1',
             'receiver': 'test2'}

MESSAGES = {'sender': ['Halo', 'Apa kabar?']}


def users(db):
    user_id = []
    for u in USER_NAME.values():
        data = Login(**{'name': u})
        user = insert_user(data, db)
        user_id.append(user.id)

    return user_id


def chat_room(sender_id, receiver_id, db):
    data = UserRoom(**{'sender': sender_id,
                       'receiver': receiver_id})
    return insert_room(data, db)


def messages(room, sender_id, db):
    msgs = []

    for m in MESSAGES['sender']:
        msg = insert_message(user_id=sender_id, content=m, db=db)
        update_messages_in_room(id=room.id, message_id=msg.id, db=db)
        msgs.append(msg)

    return msgs
