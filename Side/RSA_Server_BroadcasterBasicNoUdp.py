import asyncio
import websockets
import random
import string


list_of_connecteds_clients = []

async def broadcast_data(websocket, path):
    global list_of_connecteds_clients
    websocket_address= websocket.remote_address
    print(f"New client connected{websocket_address}")
    list_of_connecteds_clients.append(websocket)
    print(f"Connection count : {len(list_of_connecteds_clients)}")

    while True:
        # Generate random bytes and string
        random_bytes = bytes(random.randint(0, 255) for _ in range(10))
        random_string = ''.join(random.choices(string.ascii_letters, k=10))

        # Broadcast the data to all connected clients
        if not websocket.open:
            break
        await websocket.send(random_bytes)
        await websocket.send(random_string)

        # Wait for 1 second before sending the next data
        await asyncio.sleep(1)
    print(f"Client disconnected{websocket_address}")
    list_of_connecteds_clients.remove(websocket)
    print(f"Connection count : {len(list_of_connecteds_clients)}")

# Start the WebSocket server
start_server = websockets.serve(broadcast_data, '0.0.0.0', 4504)





# Run the server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()