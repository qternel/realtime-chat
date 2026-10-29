from typing import Annotated

from fastapi import APIRouter, Depends, Path, WebSocket, WebSocketDisconnect

from server.services.auth_service import AuthService
from server.services.chat_service import ChatService, get_chat_service

router = APIRouter()


@router.websocket("/ws/{room_id}")
async def chat(
    websocket: WebSocket,
    room_id: Annotated[int, Path(ge=0)],
    user_data: Annotated[tuple[int, str], Depends(AuthService.verify_jwt)],
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
):
    user_id, username = user_data
    await chat_service.connect(websocket, room_id, user_id)

    try:
        while True:
            data = await websocket.receive_text()
            await chat_service.broadcast(room_id, username, data)
    except WebSocketDisconnect:
        chat_service.disconnect(room_id, websocket)
