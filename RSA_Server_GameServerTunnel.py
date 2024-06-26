import asyncio
import websockets
import socket
import requests
import uuid
import base64
import time
import xml.etree.ElementTree as ET
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
import threading
import os

server_port = 8765
server_ipv4 = "0.0.0.0"


use_debug_print_message_udp=False
use_debug_print_message_ws=False

bool_use_local_keys = True

if bool_use_local_keys:
    public_rsa_key_pem_path= "Key/RSA_PUBLIC_PEM.txt"
    public_rsa_key_xml_path= "Key/RSA_PUBLIC_XML.txt"
else:
    public_rsa_key_pem_path= "C:\\RSA_KEYS\\TUNNELING\\RSA_PUBLIC_PEM.txt"
    public_rsa_key_xml_path= "C:\\RSA_KEYS\\TUNNELING\\RSA_PUBLIC_XML.txt"


def remove_space_line_return(text):
    text = text.replace("\n", "")
    text = text.replace(" ", "")
    return text

if os.path.exists(public_rsa_key_pem_path):
        with open(public_rsa_key_pem_path, 'r') as file:
            public_rsa_key_pem = file.read()
            print (f"Public RSA key loaded from {public_rsa_key_pem_path}")

if os.path.exists(public_rsa_key_xml_path):
        with open(public_rsa_key_xml_path, 'r') as file:
            public_rsa_key_xml = file.read()
            print (f"Public RSA key loaded from {public_rsa_key_xml_path}")


public_rsa_key_xml = """<RSAKeyValue><Modulus>vP7yDAkjkLrO7zqlaOlVpi3h7knD2xU4voEj3w9aJ9Pm/J0WADOOpnGcBc25VI7yuZuJZjsLuK9dz6aFVQR2+ZpT7H1aD/7qgXG10eIrOSu41ZIpcO26VDFcfsX1as7kmAQmLqFFTzcL2Yzv5Vz3982QeFy5Sx4MIRa26fbrKOE=</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"""
public_rsa_key_pem = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC8/vIMCSOQus7vOqVo6VWmLeHu
ScPbFTi+gSPfD1on0+b8nRYAM46mcZwFzblUjvK5m4lmOwu4r13PpoVVBHb5mlPs
fVoP/uqBcbXR4is5K7jVkilw7bpUMVx+xfVqzuSYBCYuoUVPNwvZjO/lXPf3zZB4
XLlLHgwhFrbp9uso4QIDAQAB
-----END PUBLIC KEY-----"""


public_rsa_key_xml= remove_space_line_return(public_rsa_key_xml)

public_key_imported_RSA = RSA.import_key(public_rsa_key_pem)
websockets_signed_verified=None


print(f"\n\nPublic RSA key PEM:\n{public_rsa_key_pem}\n\n")
print(f"\n\nPublic RSA key XML:\n{public_rsa_key_xml}\n\n")


queue_udp_text = []
queue_udp_bytes = []


long_received_from_tunnel_byte=0
long_push_in_tunnel_byte=0

def received_bytes(bytes_count):
    global long_received_from_tunnel_byte
    long_received_from_tunnel_byte+=bytes_count

def push_bytes(bytes_count):
    global long_push_in_tunnel_byte
    long_push_in_tunnel_byte+=bytes_count



listen_udp_text_port=4566
listen_udp_byte_port=7899
listen_udp_ivp4_bind="0.0.0.0"
listen_udp_ivp4_bind="192.168.1.250"
listen_udp_ivp4_bind="127.0.0.1"

buffer_size_bytes=1024
buffer_size_text=1024

ports_text = [7299]
ports_bytes = [7399]


def broadcast_udp_text(message_text):
    message_bytes = message_text.encode('utf-8')
    for port in ports_text:
        udp_sockett = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sockett.sendto(message_bytes, (listen_udp_ivp4_bind, port))
    if len(message_text)<128:
        if use_debug_print_message_ws:
           print(f"Broadcasted UDP text message: {message_text}")
    else:
        if use_debug_print_message_ws:
            print(f"Broadcasted UDP text message: {len(message_text)}")

def broadcast_udp_bytes(message_bytes):
    for port in ports_bytes:
        udp_socketb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socketb.sendto(message_bytes, (listen_udp_ivp4_bind, port))
    if len(message_bytes)<20:
        if use_debug_print_message_ws:
            print(f"Broadcasted UDP bytes message: {message_bytes}")
    else:
        if use_debug_print_message_ws:     
           print(f"Broadcasted UDP bytes message: {len(message_bytes)}")


def udp_listener_text():
    
    global websockets_signed_verified
    if use_debug_print_message_udp:
        print(f"UDP text Listener started {listen_udp_text_port}")
    udp_sockett = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sockett.bind((listen_udp_ivp4_bind, listen_udp_text_port))
    while True:
        data, addr = udp_sockett.recvfrom(buffer_size_text)
        
        if use_debug_print_message_udp:
            print(f"Received UDP text message from {addr}: {len(data)}")
        queue_udp_text.append(data.decode('utf-8'))
        

def udp_listener_bytes():
    global websockets_signed_verified
    if use_debug_print_message_udp:
        print(f"UDP bytes Listener started {listen_udp_byte_port}")
    udp_socketb = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socketb.bind((listen_udp_ivp4_bind, listen_udp_byte_port))
    while True:
        data, addr = udp_socketb.recvfrom(buffer_size_bytes)
        if use_debug_print_message_udp:
            print(f"Received UDP bytes message from {addr}: {len(data)}")
        queue_udp_bytes.append(data)

  
udp_threadt = threading.Thread(target=udp_listener_text)
udp_threadt.start()
udp_threadb = threading.Thread(target=udp_listener_bytes)
udp_threadb.start()

def verify_signature( message_text, signature_b64_text):
    global public_key_imported_RSA
    message_bytes= message_text.encode('utf-8')
    signature_bytes = base64.b64decode(signature_b64_text)
    hash_obj = SHA256.new(message_bytes)

    # Verify the signature using the public key
    verifier = pkcs1_15.new(public_key_imported_RSA)
    try:
        verifier.verify(hash_obj, signature_bytes)
        return True
    except (ValueError, TypeError):
        return False



async def handle_client(websocket, path):
    print("\n\n\n\n")
    print (f"New client connected: {websocket.remote_address}")
    print (f"Path: {path}")
    print (f"Websocket: {websocket}")
    print("\n\n-----------------\n\n")
    
    global websockets_signed_verified
    client_connected_verified = False
    guid_of_client_text = str(uuid.uuid4())
    # Handle incoming messages from the client

    try :
        async for message in websocket:
            if isinstance(message, str):
                if not client_connected_verified:
                    if message.startswith("Hello "):
                        print("\n\n\n\n")
                        print("\t> RECEVIED RSA HELLO REQUEST")
                        print(message)
                        
                        str_rsa_key_proposed= message[6:]
                        if str_rsa_key_proposed==public_rsa_key_pem or str_rsa_key_proposed==public_rsa_key_xml:

                            print("\n\n\n\n")
                            print("\t> SENT SIGNIN REQUEST TO CLIENT")
                            sign_message = f"SIGNIN:{guid_of_client_text}"
                            print(sign_message)
                            await websocket.send(sign_message)
                            

                        else:

                            print("\n\n\n\n")
                            print("\t> FAILED: NOT THE RIGHT RSA KEY!")                
                            await websocket.send("Invalid RSA key")
                            await websocket.close()
                            

                    elif message.startswith("SIGNED:"):
                        signature_as_byte = message[7:]

                        print("\n\n\n\n")
                        print("\t> START CHECKING SIGNATURE")
                        print(message)
                        
                        b64 = message[7:]
                        if verify_signature(guid_of_client_text, b64):
                            print("=V= Signature matches and signed")
                            print("\n\n---------------------\n\n")
                            await websocket.send("RSA:Verified")
                            await websocket.send("IndexLock:None")
                            client_connected_verified = True
                            websockets_signed_verified = websocket
                            print(f"\n\n {websocket}\n\n")
                        else :
                            print("=X= Signature does not match")
                            print("\n\n---------------------\n\n")
            
                            await websocket.send("Signature does not match")
                            await websocket.close()
                elif client_connected_verified!=None:
                    if use_debug_print_message_ws:
                        if  len(message) <128:
                            print(f"Received WS verified text message : {len(message)}")
                            print(f">:{message}")
                        else:
                            print(f"Received WS verified text message : {len(message)}")
                    received_bytes(len(message))
                    broadcast_udp_text(message)


            elif client_connected_verified!=None:
                if use_debug_print_message_ws:
                    print(f"Received WS verified binary message:{len(message)}")
                received_bytes(len(message))
                broadcast_udp_bytes(message)
    except Exception as e:
        if e != None:
                
            print("\n\n-----------------\n\n")
            print(f"Exception {e}")
            print("\n-----------------\n")

    finally:

        print("\n-----------------\n")
        print(f"Client disconnected: {websocket.remote_address}")
        print("\n\n-----------------\n\n")
        if websocket.open==True:
            await websocket.close()
        if websockets_signed_verified==websocket:
            websockets_signed_verified=None
            
            


async def get_public_ip():

    return str(requests.get('https://api.ipify.org?').content.decode('utf-8'))


async def start_server():

    # Start the WebSocket server

    # Get the public IP address of the server

    string_public_ip = await get_public_ip()

    print(f"Public IP address: {string_public_ip}")
    

    # Get the local IP address of the server

    local_ip = socket.gethostbyname(socket.gethostname())

    print(f"Local IP address: {local_ip}")
    
    

    while True:

        server=None
        try:

            server = await websockets.serve(handle_client, server_ipv4, server_port)

            print(f"WebSocket server started: {server_port}")
            

            await server.wait_closed()

        except Exception as e:
            if e != None:
                print(f"Exception:{e}")

        finally:

            print(f"\n\n\n\n-------------\nSERVER CLOSED:\n\n\n\n-------------\n")
            if server!=None and  server.open==True:
                await server.close()



# Run the WebSocket server


async def send_messages():
        while True:
            await asyncio.sleep(0.001)  # Send a message every 5 seconds
            if(len(queue_udp_text)>0 or len(queue_udp_bytes)>0):
                print(f"Tick: {time.time()}")
                qt =queue_udp_text.copy()
                qb=queue_udp_bytes.copy()
                for message in qt:
                    if websockets_signed_verified!=None:
                        await websockets_signed_verified.send(message)
                        push_bytes(len(message))
                        print (f"Sent message to client Text: {message}")
                for message in qb:
                    if websockets_signed_verified!=None:
                        await websockets_signed_verified.send(message)
                        push_bytes(len(message))
                        print (f"Sent message to client bytes: {message}")  
                queue_udp_bytes.clear()
                queue_udp_text.clear()  
            



async def ping_megabytes():
        while True:
            await asyncio.sleep(5)  # Send a message every 5 seconds           
            if long_received_from_tunnel_byte>1024**4 :
                print(f"R:\t{long_received_from_tunnel_byte/1024**4}GB P:\t{long_push_in_tunnel_byte/1024**4}GB")
            elif long_received_from_tunnel_byte>1024**3 :
                print(f"R:\t{long_received_from_tunnel_byte/1024**3}MB P:\t{long_push_in_tunnel_byte/1024**3}MB")
            elif long_received_from_tunnel_byte>1024**2 :
                print(f"R:\t{long_received_from_tunnel_byte/1024**2}KB P:\t{long_push_in_tunnel_byte/1024**2}KB")
            elif long_received_from_tunnel_byte>1024**1 :
                print(f"R:\t{long_received_from_tunnel_byte/1024}KB P:\t{long_push_in_tunnel_byte/1024}KB")
            else:
                print(f"R:\t{long_received_from_tunnel_byte} P:\t{long_push_in_tunnel_byte}")
                
            if websockets_signed_verified!=None:
                ping_text= f"PING {time.time()}"
                #print(f"PING: {ping_text}")
                push_bytes(len(ping_text))
                await websockets_signed_verified.send(ping_text.encode('utf-8'))
            

async def main():
    # Create the tasks
    t1 = asyncio.create_task(send_messages())
    t2 = asyncio.create_task(start_server())
    t3 = asyncio.create_task(ping_megabytes())

    # Wait for both tasks to complete (they won't, since they're infinite loops)
    await asyncio.gather(t1, t2,t3)

# Run the main function
asyncio.run(main())