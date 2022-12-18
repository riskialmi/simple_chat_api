from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketState

from app.api import router as api_router
from app.controllers.websocket import ConnectionManager
from app.controllers.rooms import upload_message_to_room, update_last_seen
from app.db.database import get_db

import json



app = FastAPI(title="Simple Chat API", docs_url="/docs", version="1.0.0")

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()

@app.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        await manager.connect(websocket)

        data = {
            "user_id": user_id,
            "room_id": room_id,
            "type": "entrance"
        }
        await manager.broadcast(f"{json.dumps(data, default=str)}")

        # wait for messages
        while True:
            if websocket.application_state == WebSocketState.CONNECTED:
                message = await websocket.receive_text()

                if message:
                    data['content'] = message
                    await upload_message_to_room(data, db)
                    await manager.broadcast(message)
            else:
                await manager.connect(websocket)
    except WebSocketDisconnect:
        update_last_seen(room_id, user_id, db)
        manager.disconnect(websocket)

app.include_router(api_router, prefix="/api")
