from sqlalchemy.orm import Session
from copy import copy

from app.api.crud.messages import get_message_by_id
from tests.api_objectivies.populate_data import MESSAGES


def get_messages(room, db: Session):
    msg = []
    for msg_id in room.messages:
        msg.append(get_message_by_id(id=msg_id, db=db).content)

    return msg

def test_scenario_1(client, conversation, db):
    messages = get_messages(conversation['room'], db)
    # existing conversation
    assert messages == MESSAGES['sender']

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
    expected_conv = MESSAGES['sender'].copy()
    expected_conv.append(text)
    messages = get_messages(conversation['room'], db)

    assert messages == expected_conv
