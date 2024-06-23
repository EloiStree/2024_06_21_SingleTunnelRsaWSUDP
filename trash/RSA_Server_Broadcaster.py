import asyncio
import websockets
import socket
import random

clients_websocket_set = set()

async def register(websocket):
    clients_websocket_set.add(websocket)

async def udp_listener_binary():
    udp_ip = "127.0.0.1"  # Listen on all available network interfaces
    udp_port = 7399

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((udp_ip, udp_port))
    print(f"Listening for UDP binary packets on {udp_ip}:{udp_port}")

    loop = asyncio.get_event_loop()
    while True:
        data, addr = await loop.run_in_executor(None, udp_socket.recvfrom, 4096)
       
        print(f"Received binary from {addr}: {len(data)}")
        if clients_websocket_set:
            await asyncio.wait([client.send(data) for client in clients_websocket_set])

async def udp_listener_text():
    udp_ip = "127.0.0.1"  # Listen on all available network interfaces
    udp_port = 7299

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((udp_ip, udp_port))
    print(f"Listening for UDP text packets on {udp_ip}:{udp_port}")

    loop = asyncio.get_event_loop()
    while True:
        data, addr = await loop.run_in_executor(None, udp_socket.recvfrom, 4096)
        message = data.decode()
        if(len(message) <40):
            print(f"Received message from {addr}: {message}")
        else :
            print(f"Received message from {addr}: {len(message)}")

        if clients_websocket_set:
            await asyncio.wait([client.send(message) for client in clients_websocket_set])

async def websocket_handler(websocket, path):
    await register(websocket)
    print(f"New WebSocket client connected from {websocket.remote_address}")
    while True:
        try:
            message = await websocket.recv()
            print(f"Received message from WebSocket client: {message}")
        except websockets.ConnectionClosed:
            print(f"WebSocket client disconnected from {websocket.remote_address}")
            clients_websocket_set.remove(websocket)
            break

async def push_random_value_tdd():
    loop = asyncio.get_event_loop()
    while True:
        await asyncio.sleep(1)
        if clients_websocket_set:
            data = "Hello from TDD "+str(loop.time())
            await asyncio.wait([client.send(data) for client in clients_websocket_set])
        await asyncio.sleep(1)
        if clients_websocket_set:
            data= random.randint(1,100).to_bytes(4, byteorder='little')
            await asyncio.wait([client.send(data) for client in clients_websocket_set])
        

async def main():
    udp_task_binary = asyncio.create_task(udp_listener_binary())
    udp_task_text = asyncio.create_task(udp_listener_text())
    tdd = asyncio.create_task(push_random_value_tdd())
    websocket_server = await websockets.serve(websocket_handler, "0.0.0.0", 4504)
    print(f"WebSocket server listening on port 4504")
    await asyncio.gather(udp_task_binary, tdd, udp_task_text, websocket_server.wait_closed())

if __name__ == "__main__":
    asyncio.run(main())
