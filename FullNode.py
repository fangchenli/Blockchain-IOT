from KeyUtils import *
from Transaction import TxDB


class FullNode:

    def __init__(self):
        # generate keys for ecc
        self.private_key_ecc = generate_private_key_ecc()
        self.public_key_ecc = generate_public_key_ecc(self.private_key_ecc)

        # generate keys for rsa
        self.private_key_rsa = generate_private_key_rsa()
        self.public_key_rsa = generate_public_key_rsa(self.private_key_rsa)

        # connected full nodes
        self.heavy_peers_limit = 10
        self.heavy_peers = []

        # connected full nodes
        self.light_peers_limit = 10
        self.light_peers = []

        # transaction database
        self.tx_db = TxDB()
