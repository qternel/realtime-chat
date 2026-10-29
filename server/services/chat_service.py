from datetime import datetime, timezone

from fastapi import WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder

from server.models.chat import Message, MessagePayload


class ChatService:
    def __init__(self):
        self.active_connections: dict[int, set[WebSocket]] = (
            {}
        )  # room id -> dict[user id, websocket]

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        await websocket.accept()
        self.active_connections.setdefault(room_id, set()).add(websocket)

    def disconnect(self, room_id: int, websocket: WebSocket):
        self.active_connections[room_id].remove(websocket)

    async def broadcast(self, room_id: int, username: str, message_text: str):
        for ws in self.active_connections[room_id]:
            await ws.send_json(
                jsonable_encoder(
                    MessagePayload(
                        message=Message(
                            username=username,
                            text=message_text,
                            sent_at=datetime.now(timezone.utc),
                        )
                    )
                )
            )


chat_service = ChatService()


def get_chat_service():
    return chat_service
