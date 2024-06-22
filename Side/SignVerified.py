import hashlib
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Public RSA key (in PEM format)
public_rsa_key_pem = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC8/vIMCSOQus7vOqVo6VWmLeHu
ScPbFTi+gSPfD1on0+b8nRYAM46mcZwFzblUjvK5m4lmOwu4r13PpoVVBHb5mlPs
fVoP/uqBcbXR4is5K7jVkilw7bpUMVx+xfVqzuSYBCYuoUVPNwvZjO/lXPf3zZB4
XLlLHgwhFrbp9uso4QIDAQAB
-----END PUBLIC KEY-----"""

private_rsa_key_pem = """-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBALz+8gwJI5C6zu86
pWjpVaYt4e5Jw9sVOL6BI98PWifT5vydFgAzjqZxnAXNuVSO8rmbiWY7C7ivXc+m
hVUEdvmaU+x9Wg/+6oFxtdHiKzkruNWSKXDtulQxXH7F9WrO5JgEJi6hRU83C9mM
7+Vc9/fNkHhcuUseDCEWtun26yjhAgMBAAECgYEAoJ3J9pCNuSIJWyXsDQy/zUqR
B4GJAVc3si7t3VOeutpLI8QcPm+Se8FxZz0+k64oebTFQCxN+daPUzmhdm8k6+Oq
oYV/gHCrWbEQMAKkavT3rxtlJbkWkFgqNxmMQA2/2feC0ESbavtZemBLOP7p+VVr
/cYu6DzpUNr5+FVhD0ECQQDHn5vzi3oNTt2ZGdluDqcrl4vIax4jINWh1qtDx/sL
iQJN+BgbtZbz1fVxT/+MyyPeaNCe06MkXYGSG1f8dY7TAkEA8l77YEBBJiLo6yuF
DZLWRyjYJsEvuE3/MQvSwXtY2Hb7BM+ynhIcncs6jGmUuSSNoXhQ877CeD2sOJbG
V+Ng+wJAJ98nZRO8wx+3fzb8iNEAbuKMFvHeSSHrybF478bny7wH687b8dzpU7au
mX1jC5ofhfLliHO5KDBNCwPPJSvN5QJAOzKVxUmMYAswxpfHlKwjqBfCy5xt0l9C
kDEqFdXRunU9FEzCfLdBxAyqTTdQevQBn8mqRA54ozO1B9FTuo2v1wJAK+5TNsF1
zM4SeFX8Pd7OcsB3yYP0VkCCawyeQxjm3GQbQd805JnqCoaAnAiuM5N49jonQXuJ
MjYqgxT0JWh2VA==
-----END PRIVATE KEY-----"""
# Public RSA key (in PEM format)
public_rsa_key_pem = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC8/vIMCSOQus7vOqVo6VWmLeHu
ScPbFTi+gSPfD1on0+b8nRYAM46mcZwFzblUjvK5m4lmOwu4r13PpoVVBHb5mlPs
fVoP/uqBcbXR4is5K7jVkilw7bpUMVx+xfVqzuSYBCYuoUVPNwvZjO/lXPf3zZB4
XLlLHgwhFrbp9uso4QIDAQAB
-----END PUBLIC KEY-----"""

private_rsa_key_pem = """-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBALz+8gwJI5C6zu86
pWjpVaYt4e5Jw9sVOL6BI98PWifT5vydFgAzjqZxnAXNuVSO8rmbiWY7C7ivXc+m
hVUEdvmaU+x9Wg/+6oFxtdHiKzkruNWSKXDtulQxXH7F9WrO5JgEJi6hRU83C9mM
7+Vc9/fNkHhcuUseDCEWtun26yjhAgMBAAECgYEAoJ3J9pCNuSIJWyXsDQy/zUqR
B4GJAVc3si7t3VOeutpLI8QcPm+Se8FxZz0+k64oebTFQCxN+daPUzmhdm8k6+Oq
oYV/gHCrWbEQMAKkavT3rxtlJbkWkFgqNxmMQA2/2feC0ESbavtZemBLOP7p+VVr
/cYu6DzpUNr5+FVhD0ECQQDHn5vzi3oNTt2ZGdluDqcrl4vIax4jINWh1qtDx/sL
iQJN+BgbtZbz1fVxT/+MyyPeaNCe06MkXYGSG1f8dY7TAkEA8l77YEBBJiLo6yuF
DZLWRyjYJsEvuE3/MQvSwXtY2Hb7BM+ynhIcncs6jGmUuSSNoXhQ877CeD2sOJbG
V+Ng+wJAJ98nZRO8wx+3fzb8iNEAbuKMFvHeSSHrybF478bny7wH687b8dzpU7au
mX1jC5ofhfLliHO5KDBNCwPPJSvN5QJAOzKVxUmMYAswxpfHlKwjqBfCy5xt0l9C
kDEqFdXRunU9FEzCfLdBxAyqTTdQevQBn8mqRA54ozO1B9FTuo2v1wJAK+5TNsF1
zM4SeFX8Pd7OcsB3yYP0VkCCawyeQxjm3GQbQd805JnqCoaAnAiuM5N49jonQXuJ
MjYqgxT0JWh2VA==
-----END PRIVATE KEY-----"""

def sign_message(private_key, message):
    # Create a hash object using SHA256 and hash the message
    hash_obj = SHA256.new(message)

    # Sign the hash using the private key
    signer = pkcs1_15.new(private_key)
    signature = signer.sign(hash_obj)

    return signature

def verify_signature(public_key, message, signature):
    # Create a hash object using SHA256 and hash the message
    hash_obj = SHA256.new(message)

    # Verify the signature using the public key
    verifier = pkcs1_15.new(public_key)
    try:
        verifier.verify(hash_obj, signature)
        return True
    except (ValueError, TypeError):
        return False

# Generate a private key (for demonstration purposes)
private_key = RSA.import_key(private_rsa_key_pem)

# Load the public RSA key from PEM format
public_key = RSA.import_key(public_rsa_key_pem)

# Message to be signed
message = b'This is a test message.'

# Sign the message using the private key
signature = sign_message(private_key, message)

# Print the signature
print("Signature:", signature)

# Verify the signature using the public key
is_valid = verify_signature(public_key, message, signature)
if is_valid:
    print("Signature is valid.")
else:
    print("Signature is invalid.")
