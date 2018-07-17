
from ecdsa import SigningKey, SECP256k1

from hashlib import sha256

from base64 import b64encode, b64decode

# comments:
# BTC uses base58 encode to avoid special characters. It requires another library. So I use base64 here.


def generate_private_key():
    """
    generate a private key using SECP256k1 curve and sha256 encryption
    :return: a private key of type ecdsa.SigningKey
    """
    return SigningKey.generate(curve=SECP256k1, hashfunc=sha256)


def generate_public_key(private_key):
    """
    given a private key, generate its public key
    :param private_key: a private key of type ecdsa.SigningKey
    :return: a public key of type ecdsa.VerifyingKey
    """
    return private_key.get_verifying_key()


def key_to_address(key):
    """
    encode a key to address using base64
    :param key:
    :return:
    """
    return b64encode(key.to_string())


def address_to_key(address):
    """
    decode an address to key using base64 in hex format
    :param address:
    :return:
    """
    return b64decode(address, validate=True).hex()


def test():
    sk = generate_private_key()  # generate private key

    vk = generate_public_key(sk)  # generate public key

    sadd = key_to_address(sk)  # convert private key to address

    vadd = key_to_address(vk)  # convert public key to address

    print('\nprivate key: ' + sk.to_string().hex())

    print('\nconvert to address: ')
    print(sadd)

    print('\nconvert back to key: ' + address_to_key(sadd))

    print('\npublic key: ' + vk.to_string().hex())

    print('\nconvert to address: ')
    print(vadd)

    print('\nconvert back to key: ' + address_to_key(vadd))

    message = "hello world."  # get a message
    print('\nmessage: ' + message)

    signature = sk.sign(message.encode('utf-8'))  # sign a signature using private key
    print('\nsign a signature: ' + signature.hex())

    # verify the message using the public key
    print('\nverify the message and signature using the public key: ')
    print(vk.verify(signature, message.encode('utf-8')))


if __name__ == '__main__':
    test()
