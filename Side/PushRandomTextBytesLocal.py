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



def listen_udp(port, is_text=False):
            # Create a socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Bind the socket to the specified port
            sock.bind(("0.0.0.0", port))

            while True:
                # Receive data from the socket
                data, addr = sock.recvfrom(1024)
                if is_text:
                    # Decode the received data
                    text = data.decode("utf-8")

                    print(f"Received text: {text}")
                else:
                    # Print the received byte array
                    print(f"Received byte array: {data}")

                # Process the received data
                # TODO: Add your code here to process the received data

        # Create a thread for listening to port 7299
udp_thread = threading.Thread(target=listen_udp, args=(7399,False))
udp_thread.start()
udp_thread = threading.Thread(target=listen_udp, args=(7299,True))
udp_thread.start()





while True:
    time.sleep(3)
    push_byte_array("127.0.0.1", 7399)
    # time.sleep(3)
    # push_text_random("127.0.0.1",4566)
    
    
