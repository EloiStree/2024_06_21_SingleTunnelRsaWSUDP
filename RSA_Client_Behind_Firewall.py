# pip install pycryptodomex
# https://pycryptodome-master.readthedocs.io/en/latest/src/installation.html
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


private_rsa_key_xml ="""<RSAKeyValue><Modulus>vP7yDAkjkLrO7zqlaOlVpi3h7knD2xU4voEj3w9aJ9Pm/J0WADOOpnGcBc25VI7yuZuJZjsLuK9dz6aFVQR2+ZpT7H1aD/7qgXG10eIrOSu41ZIpcO26VDFcfsX1as7kmAQmLqFFTzcL2Yzv5Vz3982QeFy5Sx4MIRa26fbrKOE=</Modulus><Exponent>AQAB</Exponent><P>x5+b84t6DU7dmRnZbg6nK5eLyGseIyDVodarQ8f7C4kCTfgYG7WW89X1cU//jMsj3mjQntOjJF2BkhtX/HWO0w==</P><Q>8l77YEBBJiLo6yuFDZLWRyjYJsEvuE3/MQvSwXtY2Hb7BM+ynhIcncs6jGmUuSSNoXhQ877CeD2sOJbGV+Ng+w==</Q><DP>J98nZRO8wx+3fzb8iNEAbuKMFvHeSSHrybF478bny7wH687b8dzpU7aumX1jC5ofhfLliHO5KDBNCwPPJSvN5Q==</DP><DQ>OzKVxUmMYAswxpfHlKwjqBfCy5xt0l9CkDEqFdXRunU9FEzCfLdBxAyqTTdQevQBn8mqRA54ozO1B9FTuo2v1w==</DQ><InverseQ>K+5TNsF1zM4SeFX8Pd7OcsB3yYP0VkCCawyeQxjm3GQbQd805JnqCoaAnAiuM5N49jonQXuJMjYqgxT0JWh2VA==</InverseQ><D>oJ3J9pCNuSIJWyXsDQy/zUqRB4GJAVc3si7t3VOeutpLI8QcPm+Se8FxZz0+k64oebTFQCxN+daPUzmhdm8k6+OqoYV/gHCrWbEQMAKkavT3rxtlJbkWkFgqNxmMQA2/2feC0ESbavtZemBLOP7p+VVr/cYu6DzpUNr5+FVhD0E=</D></RSAKeyValue>"""
public_rsa_key_xml = """<RSAKeyValue><Modulus>vP7yDAkjkLrO7zqlaOlVpi3h7knD2xU4voEj3w9aJ9Pm/J0WADOOpnGcBc25VI7yuZuJZjsLuK9dz6aFVQR2+ZpT7H1aD/7qgXG10eIrOSu41ZIpcO26VDFcfsX1as7kmAQmLqFFTzcL2Yzv5Vz3982QeFy5Sx4MIRa26fbrKOE=</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"""
public_rsa_key_pem = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC8/vIMCSOQus7vOqVo6VWmLeHu
ScPbFTi+gSPfD1on0+b8nRYAM46mcZwFzblUjvK5m4lmOwu4r13PpoVVBHb5mlPs
fVoP/uqBcbXR4is5K7jVkilw7bpUMVx+xfVqzuSYBCYuoUVPNwvZjO/lXPf3zZB4
XLlLHgwhFrbp9uso4QIDAQAB
-----END PUBLIC KEY-----"""


print (f"Private key in XML format:\n{private_rsa_key_xml}\n")
print (f"Public key in XML format:\n{public_rsa_key_xml}\n")
print (f"Public key in PEM format:\n{public_rsa_key_pem}\n")

# Remove newlines, carriage returns, tabs, and spaces from the public key XML
public_rsa_key_xml = public_rsa_key_xml.replace("\n","").replace("\r","").replace("\t","").replace(" ","")

# Import the public key as an RSA object
public_key_imported_RSA = RSA.import_key(public_rsa_key_pem)

async def connect_to_websocket():
    uri = "ws://81.240.94.97:8765"  # Replace with the actual IP address and port

    print (f"Connecting to {uri}...")
    async with websockets.connect(uri) as websocket:
        
        
        await websocket.send("Hello "+public_rsa_key_xml)
        response = await websocket.recv()
        print(f"Received message from server: {response}")
        if response.startswith("SIGNIN:"):
            toSignGUID = response.replace("SINGIN:","")
            GUIDASBYTES = toSignGUID.encode('utf-8')
            
            
            #signature = pkcs1_15.new(private_rsa_key_xml).sign(SHA256.new(GUIDASBYTES))
            #### FAIL HERE
            private_key = RSA.import_key(private_rsa_key_xml)
            signer = pkcs1_15.new(private_key)
            signature = signer.sign(SHA256.new(GUIDASBYTES))
            
            
            messageSignedAsB64 = base64.b64encode(signature).decode('utf-8')
            print(f"Sending signed message to server: SIGNED:{messageSignedAsB64}")
            await websocket.send("SIGNED:"+messageSignedAsB64)
            response = await websocket.recv()
            print(f"Received message from server: {response}")
            response = await websocket.recv()
            

print("Hello from the client!")
# Run the WebSocket client
asyncio.run(connect_to_websocket())