import multiprocessing
import time

def test_scenario_1(client, initial_data):
    with client.websocket_connect(f"/ws/{initial_data['room'].id}/{initial_data['sender_id']}") as websocket:
        entered_chat = websocket.receive_json()

        text = 'Halo'
        websocket.send_text(text)
        receive_text = websocket.receive_text()

        assert entered_chat == {
            "user_id": initial_data['sender_id'],
            "room_id": initial_data['room'].id,
            "type": "entrance"
        }

        assert receive_text == text

def test_scenario_2(client, initial_data):
    # connection still open and websocket keep waiting for incoming message
    with client.websocket_connect(f"/ws/{initial_data['room'].id}/{initial_data['sender_id']}") as websocket:
        entered_chat = websocket.receive_json()

        assert entered_chat == {
            "user_id": initial_data['sender_id'],
            "room_id": initial_data['room'].id,
            "type": "entrance"
        }


        text = ''
        websocket.send_text(text)

        # keep waiting incoming messages
        proses = multiprocessing.Process(target=websocket.receive_text, name='receive text')
        proses.start()

        # waiting incoming messages
        time.sleep(0.1)

        # stop receiving messages
        proses.terminate()






