from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# generate keys
key_length = 1024  # It must be a multiple of 256, and no smaller than 1024.
keys = RSA.generate(key_length)
public_key = keys.publickey()

# ---------------------------------sender---------------------------------
# generate cipher from public key
cipher_sender = PKCS1_OAEP.new(public_key)

# create message
message = 'hello world.'

# encrypt message
message_encrypted = cipher_sender.encrypt(message.encode('utf-8'))

print(message_encrypted.hex())

# -------------------------------recipient-------------------------------
# generate cipher from private key
cipher_recipient = PKCS1_OAEP.new(keys)

# decrypt message
message_decrypted = cipher_recipient.decrypt(message_encrypted)

print(message_decrypted)

exp_public_key = public_key.exportKey()

print(type(exp_public_key.decode('utf-8')))
print(exp_public_key.decode('utf-8'))

inp_public_key = RSA.importKey(exp_public_key)

print(inp_public_key.has_private())
