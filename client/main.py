import asyncio
import json
from datetime import datetime

import httpx2
import websockets
from dateutil import parser

WS_URL = "ws://localhost:8000/api/ws"


async def recieve_messages(websocket: websockets.connect):
    try:
        async for raw_message in websocket:
            response = json.loads(raw_message).get("message", {})

            username = response.get("username", "")
            sent_at = parser.isoparse(response.get("sent_at", "")).astimezone(
                datetime.now().astimezone().tzinfo
            )
            text = response.get("text", "")
            print(f"{username} at {sent_at}: {text}")
    except Exception as exc:  # websockets.ConnectionClosed
        print("\nconnection closed", exc)


async def client():
    mode = int(input("sign in or chat in guest mode (1/2): "))

    headers = {}

    if mode == 1:
        pass

    room = int(input("enter room id: "))
    ws_url_room = WS_URL + f"/{room}"

    try:
        async with websockets.connect(
            ws_url_room, additional_headers=headers
        ) as websocket:
            print("successfully connected")

            receiver_task = asyncio.create_task(recieve_messages(websocket))
            try:
                while True:
                    message = await asyncio.to_thread(input)
                    if not message:
                        continue

                    if message.strip().casefold() in {"/quit", "/exit"}:
                        print("\nconnection closed")
                        break
                    await websocket.send(message)
            except websockets.ConnectionClosed:
                print("connection closed")
            finally:
                receiver_task.cancel()

                try:
                    await receiver_task
                except asyncio.CancelledError:
                    pass

    except:
        print("\nconnection closed")


if __name__ == "__main__":
    try:
        asyncio.run(client())
    except:
        pass
