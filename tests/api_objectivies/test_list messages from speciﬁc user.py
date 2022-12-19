from typing import List
from pydantic import parse_obj_as

from tests.conftest import PREFIX
from app.api.schemas.rooms import Message, Room


def test_scenario_1(client, db, conversation):
    user = {'sender': conversation['sender_id'],
            'receiver': conversation['receiver_id']}
    expected_res = {"sender": user['sender'],
                    "receiver": user['receiver'],
                    "id": conversation['room'].id,
                    "messages": conversation['messages']
                    }

    response = client.post(PREFIX + '/room', json=user)
    res_json = response.json()

    msg_json = res_json['messages']
    messages = parse_obj_as(List[Message], msg_json)
    expected_msgs = parse_obj_as(List[Message], conversation['messages'])

    response = Room(**res_json)
    expected_res = Room(**expected_res)

    assert messages == expected_msgs
    assert response == expected_res
