from typing import List

from pydantic import parse_obj_as

from app.api.crud.messages import get_messages_by_ids, get_message_by_content
from app.api.crud.rooms import get_room_by_members
from app.api.schemas.rooms import Message
from app.api.schemas.users import UserRoom

def test_scenario_1(client, conversation, db):
    # existing conversation
    old_messages = parse_obj_as(List[Message], get_messages_by_ids(conversation['room'].messages, db))

    with client.websocket_connect(f"/ws/{conversation['room'].id}/{conversation['sender_id']}") as websocket:
        entered_chat = websocket.receive_json()

        assert entered_chat == {
            "user_id": conversation['sender_id'],
            "room_id": conversation['room'].id,
            "type": "entrance"
        }

        text = 'Saya baik, bagaimana kabarmu?'
        websocket.send_text(text)
        receive_text = websocket.receive_text()

        assert receive_text == text

    # conversation after sending message
    members = UserRoom(**{'sender': conversation['sender_id'],
                       'receiver': conversation['receiver_id']})
    msg_ids = get_room_by_members(members, db).messages
    messages = parse_obj_as(List[Message], get_messages_by_ids(msg_ids, db))

    # expected massages in conversation
    new_msg = parse_obj_as(Message, get_message_by_content(content=text, db=db))
    old_messages.append(new_msg)
    expected_conv = old_messages

    assert messages == expected_conv
