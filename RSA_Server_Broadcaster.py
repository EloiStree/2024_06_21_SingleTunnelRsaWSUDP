import asyncio
import websockets
import random
import string
import threading
import socket
import socket
import requests



server_port = 4504
udp_port_listener_binary = 7399
udp_port_listener_text = 7299
udp_ipv4_listener="127.0.0.1"


byte_pushed_count = 0
byte_received_to_push_count = 0

byte_pushed_count_frame = 0
byte_received_to_push_count_frame = 0

bool_use_print_message_received=False


print(f"Server listening on port {server_port}")
print(f"UDP binary listener on port {udp_port_listener_binary}")
print(f"UDP text listener on port {udp_port_listener_text}")

print("\n")
def print_local_ipv4():
    hostname = socket.gethostname()
    ip_addresses = socket.gethostbyname_ex(hostname)[-1]
    for ip in ip_addresses:
            print(f"Local IPv4 address: {ip}")
print_local_ipv4()

print("\n")
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to get public IP. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while getting public IP: {e}")
public_ip = get_public_ip()
if public_ip:
    print(f"Public IP address: {public_ip}")

print("\n")
print("\n")

list_of_connecteds_clients = []

async def broadcast_data(websocket, path):
    global list_of_connecteds_clients
    websocket_address= websocket.remote_address
    print(f"New client connected{websocket_address}")
    list_of_connecteds_clients.append(websocket)
    print(f"Connection count : {len(list_of_connecteds_clients)}")

    while True:
        if not websocket.open:
            break
        await asyncio.sleep(0.001)
    print(f"Client disconnected{websocket_address}")
    list_of_connecteds_clients.remove(websocket)
    print(f"Connection count : {len(list_of_connecteds_clients)}")

# Start the WebSocket server
start_server = websockets.serve(broadcast_data, '0.0.0.0', server_port)


list_bytes_to_send = []
list_text_to_send = []

async def push_data_to_clients_bytes(data:bytes):
    global byte_pushed_count
    global list_of_connecteds_clients
    global byte_received_to_push_count
    global byte_received_to_push_count_frame
    global byte_pushed_count_frame
    byte_received_to_push_count_frame+= len(data)
    byte_received_to_push_count+= len(data)
    for client in list_of_connecteds_clients:
        byte_pushed_count+= len(data)
        byte_pushed_count_frame+= len(data)
        await client.send(data)
async def push_data_to_clients_text(data:string):
    global byte_pushed_count
    global list_of_connecteds_clients
    global byte_received_to_push_count
    global byte_received_to_push_count_frame
    global byte_pushed_count_frame
    byte_received_to_push_count_frame+= len(data)
    byte_received_to_push_count+= len(data)
    for client in list_of_connecteds_clients:
        byte_pushed_count+= len(data)
        byte_pushed_count_frame+= len(data)
        await client.send(data)

def other_code_binary():
    udp_ip = udp_ipv4_listener
    udp_port = udp_port_listener_binary
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((udp_ip, udp_port))
    
    print(f"Listening for UDP Binary packets on {udp_ip}:{udp_port}")
    
    while True:
        try:
            # Receive data from the socket
            data, addr = udp_socket.recvfrom(4096)  # Buffer size is 1024 bytes
            if bool_use_print_message_received:
                if(len(data)<17):
                    print(f"Received message binary: {data} from {addr}")
                else :
                    print(f"Received message binary: {len(data)} from {addr}")
            list_bytes_to_send.append(data)
        except Exception as e:
            handle_exception_feedback(e)

def other_code_text():

    udp_ip = udp_ipv4_listener
    udp_port = udp_port_listener_text
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((udp_ip, udp_port))
    
    print(f"Listening for UDP text packets on {udp_ip}:{udp_port}")
    
    while True:
        try: 
            # Receive data from the socket
            data, addr = udp_socket.recvfrom(4096)  # Buffer size is 1024 bytes
            if bool_use_print_message_received:
                if(len(data)<17):
                    print(f"Received message text: {data} from {addr}")
                else :
                    print(f"Received message text: {len(data)} from {addr}")
            list_text_to_send.append(data.decode("utf-8" ))
        except Exception as e:
            handle_exception_feedback(e)

def handle_exception_feedback(exception:Exception):
    if exception.winerror == 10040:
        print(f"Message too big ")
    else:
        print(f"An error occurred: {exception}")

# Create a thread to run the other code
thread = threading.Thread(target=other_code_binary)
thread.start()
# Create a thread to run the other code
thread = threading.Thread(target=other_code_text)
thread.start()


async def flush_waiting_push():
    global list_bytes_to_send
    global list_text_to_send
    while True:
        if len(list_bytes_to_send) > 0:
            data = list_bytes_to_send.pop(0)
            await push_data_to_clients_bytes(data)
            #print ("Data pushed Bytes")
        if len(list_text_to_send) > 0:
            data = list_text_to_send.pop(0)
            await push_data_to_clients_text(data)
            #print ("Data pushed Text")
        await asyncio.sleep(0.001)


async def display_byte_count():
    global byte_pushed_count
    global byte_received_to_push_count
    global byte_pushed_count_frame
    global byte_received_to_push_count_frame
    p = ""
    r= ""
    while True:
        if byte_pushed_count < 1024:
            p=(f" B {byte_pushed_count}")
        elif byte_pushed_count < 1024**2:
            p=(f"KB {byte_pushed_count / 1024}")
        elif byte_pushed_count < 1024**3:
            p=(f"MB {byte_pushed_count / 1024**2}")
        else:
            p=(f"GB {byte_pushed_count / 1024**3}")

        if byte_received_to_push_count < 1024:
            r=(f"B {byte_received_to_push_count}")
        elif byte_received_to_push_count < 1024**2:
            r=(f"KB {byte_received_to_push_count / 1024}")
        elif byte_received_to_push_count < 1024**3:
            r=(f"MB {byte_received_to_push_count / 1024**2}")
        else:   
            r=(f"GB {byte_received_to_push_count / 1024**3}")

        print(f"T  P  \t{p} \tR\t{r}")
        print(f"\\S P\t{byte_pushed_count_frame} Bytes \tR\t{byte_received_to_push_count_frame} Bytes")    

        byte_pushed_count_frame=0
        byte_received_to_push_count_frame=0
        await asyncio.sleep(1)

# Create a future task for flush_waiting_push
future = asyncio.ensure_future(flush_waiting_push())


display_byte= asyncio.ensure_future(display_byte_count())

# Run the server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(future)
asyncio.get_event_loop().run_until_complete(display_byte)

asyncio.get_event_loop().run_forever()
asyncio.get_event_loop().run_forever()