from datetime import datetime, timezone

from fastapi import WebSocket, WebSocketDisconnect

from server.models.chat import Message, MessagePayload


class ChatService:
    def __init__(self):
        self.active_connections: dict[int, dict[int, WebSocket]] = (
            {}
        )  # room id -> dict[user id, websocket]

    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        await websocket.accept()
        self.active_connections.setdefault(room_id, {})[user_id] = websocket

    def disconnect(self, room_id: int, user_id: int):
        del self.active_connections[room_id][user_id]

    async def broadcast(self, room_id: int, username: str, message_text: str):
        for u_id, ws in self.active_connections[room_id].items():
            await ws.send_json(
                MessagePayload(
                    message=Message(
                        username=username,
                        text=message_text,
                        sent_at=datetime.now(timezone=timezone.utc),
                    )
                )
            )


chat_service = ChatService()


def get_chat_service():
    return chat_service
