from KeyUtils import encrypt_message, string_to_keys
from Transaction import Tx, tx_from_string
from LightWeightNode import LightWeightNode

# create two nodes
node1 = LightWeightNode()
node2 = LightWeightNode()

# now node1 wants to send a message to node2

message = 'hello world.'
print('\noriginal message: ' + message)

# First, two nodes need to make connections, and exchange public keys

# export keys to string format
keys_node1 = node1.export_keys()
keys_node2 = node2.export_keys()

# send keys to the other party, import keys and reconstruct the key object
# Todo: implement communication
ecc1, rsa1 = string_to_keys(keys_node1)
ecc2, rsa2 = string_to_keys(keys_node2)

# node1 encrypt the message using node2's public rsa key
message_encrypt = encrypt_message(rsa2, message)
print('\nencrypted message: ' + message_encrypt)

# create the transaction
tx1_at_node1 = Tx('connect', ecc1.to_string().hex(), ecc2.to_string().hex(), message_encrypt)

# while sending the transaction, using its to_string() method to convert the transaction to a json style string format
tx1_string = tx1_at_node1.to_string

print('\nThe transaction we are sending: ')
print(tx1_string)

# send this message to node2

# node2 received this message and reconstruct the transaction object
tx1_at_node2 = tx_from_string(tx1_string)

print('\nmessage: ' + str(tx1_at_node2.message))
print('sender: ' + tx1_at_node2.sender)
print('recipient: ' + tx1_at_node2.recipient)
print('content: ' + tx1_at_node2.content)
print('timestamp: ' + str(tx1_at_node2.timestamp))

# now node2 wants to decrypt the message using its own private rsa key
message_decrypt = node2.decrypt_message(tx1_at_node2.content)
print('\n' + message_decrypt)
