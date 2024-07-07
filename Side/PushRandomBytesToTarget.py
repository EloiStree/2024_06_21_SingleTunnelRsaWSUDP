import socket
import random
import uuid
import time
import threading

def push_byte_array(ip, port):
    # Generate a random byte array
    byte_array = bytearray(random.getrandbits(8) for _ in range(10))

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Send the byte array
        sock.sendto(byte_array, (ip, port))

        print("Byte array pushed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example

def push_text_random(ip, port):
  
    # Generate a random text string
    text = str(uuid.uuid4())
    byte_array= bytearray(text, "utf-8")

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Send the byte array
        sock.sendto(byte_array, (ip, port))

        print("Text  pushed successfully! \n"+text)
    except Exception as e:
        print(f"An error occurred: {e}")





while True:
    time.sleep(1)
    push_byte_array("127.0.0.1", 7399)
    time.sleep(1)
    push_text_random("127.0.0.1",7299)
    
    
