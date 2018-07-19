from json import dumps, loads
from KeyUtil import *
from Transaction import TxDB
from Crypto.Cipher import PKCS1_OAEP


class LightWeightNode:

    def __init__(self):
        # generate keys for ecc
        self.private_key_ecc = generate_private_key_ecc()
        self.public_key_ecc = generate_public_key_ecc(self.private_key_ecc)

        # generate keys for rsa
        self.private_key_rsa = generate_private_key_rsa()
        self.public_key_rsa = generate_public_key_rsa(self.private_key_rsa)

        # connected full nodes
        self.heavy_peers_limit = 1
        self.peers_heavy = []

        # connected light weight nodes
        self.light_peers_limit = 1
        self.peers_light = []

        # transaction database
        self.tx_db = TxDB()

    @staticmethod
    def import_keys(s):
        """
        Import keys from string.
        :param s: a json style string created by export_keys() method
        :return: ecc key and rsa key objects
        """
        j = loads(s)
        public_key_ecc = import_public_key_ecc(j["public_key_ecc"])
        public_key_rsa = import_public_key_rsa(j["public_key_rsa"])
        return public_key_ecc, public_key_rsa

    @staticmethod
    def encrypt_message(public_key_recipient, message):
        """
        Encrypt a message using recipient's public key
        :param public_key_recipient: public key of recipient
        :param message: message in string format
        :return: an rsa encrypted message
        """
        return PKCS1_OAEP.new(public_key_recipient).encrypt(message.encode('utf-8'))

    def export_keys(self):
        """
        Export public key and public rsa key to a string
        :return: a json style string
        """
        keys = dict([('public_key_ecc', self.export_public_key_ecc()),
                     ('public_key_rsa', self.export_public_key_rsa())])
        return dumps(keys)

    def find_peers(self):
        """
        connect to peers
        :return:
        """
        # Todo: implement, connect to full nodes and other light weight nodes
        return [], [], self

    def decrypt_message(self, message):
        """
        Decrypt an encrypted message using private key
        :param message: an rsa encrypted message
        :return: the decrypted message
        """
        return PKCS1_OAEP.new(self.private_key_rsa).decrypt(message)

    def export_public_key_ecc(self):
        """
        Export the public key to string format
        :return: a public key in string format
        """
        return self.public_key_ecc.to_string().hex()

    def export_public_key_rsa(self):
        """
        Export the public rsa key to string format
        :return: a public key in string format
        """
        return self.public_key_rsa.exportKey().decode('utf-8')


def test():
    # test rsa encryption and decryption
    lwn = LightWeightNode()
    message = 'abcdefg'
    message_en = lwn.encrypt_message(lwn.private_key_rsa, message)  # encrypt using its own node for convenience.
    print(message_en)
    message_de = lwn.decrypt_message(message_en)
    print(message_de)

    # test export
    exp_s = lwn.export_keys()
    print(exp_s)

    # test import
    p1, p2 = lwn.import_keys(exp_s)
    print(p1.to_string().hex())
    print(p2.exportKey())


if __name__ == "__main__":
    test()
