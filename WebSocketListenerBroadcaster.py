import asyncio
import websockets
import time

uri = "ws://81.240.94.97:4504"


async def connect_to_websocket():
    global uri

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    message = await websocket.recv()
                    if(message is not None and message != "" and len(message) > 0):
                        if isinstance(message, str):
                            print(f"Received text message: {message}")
                        else:
                            print(f"Received non-text message.{len(message)}")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed with exception: {e}")
        except Exception as e:
            print(f"Exception: {e}")
        time.sleep(5)
        

asyncio.get_event_loop().run_until_complete(connect_to_websocket())