import asyncio
import json

import httpx2
import websockets

WS_URL = "ws://localhost:8000/api/ws/1"


async def recieve_messages(websocket: websockets.connect):
    try:
        async for raw_message in websocket:
            response = json.loads(raw_message).get("message", {})
            print(
                f"{response.get("username")} at {response.get("sent_at")}: {response.get("text")}"
            )
    except websockets.ConnectionClosed:
        print("\nconnection closed")


async def client():
    mode = int(input("sign in or chat in guest mode (1/2): "))
    print(mode)

    headers = {}

    if mode == 1:
        pass

    try:
        async with websockets.connect(WS_URL, additional_headers=headers) as websocket:
            print("successfully connected")

            receiver_task = asyncio.create_task(recieve_messages(websocket))
            try:
                while True:
                    message = await asyncio.to_thread(input)

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
