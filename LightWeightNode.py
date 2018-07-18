from src.KeyUtil import *
from src.Transaction import TxDB
from hashlib import sha256


class LightWeightNode:

    def __init__(self):
        self.private_key = generate_private_key()
        self.public_key = generate_public_key(self.private_key)
        self.heavy_peers_limit = 1
        self.light_peers_limit = 1
        self.peers_heavy = []
        self.peers_light = []
        self.tx_db = TxDB()

    def find_peers(self):
        """
        connect to peers
        :return:
        """
        # Todo: implement, connect to full nodes and other light weight nodes
        return [], []


def calculate_hashes_map(merkle_tree_map):
    """
    Given a merkle tree map of a transaction, calculate the corresponding maps to the required transactions
    in the merkle tree for SPV.
    :param merkle_tree_map:
    """
    depth = len(merkle_tree_map)
    maps = []
    i = depth
    while i > 0:
        # for transaction at higher level, remove the last element of the tree map
        if i < depth:
            merkle_tree_map.pop()

        # reverse one step of the map to get the complimentary transaction
        merkle_tree_map[-1] *= -1

        # add to the 2-d array that stores the maps
        maps.append(merkle_tree_map.copy())

        # move counter
        i -= 1
    return maps


def confirm_tx(tx_hash, merkle_root, hashes):
    """
    Confirm if a transaction is in one block
    :param tx_hash: hash of this transaction
    :param merkle_root: the merkle root in a header of the block we are trying to confirm
    :param hashes: the corresponding transaction hashes given by the full node
    :return: true if the tx exist under given merkle root and hashes
    """

    # initialize sha256
    hash_func = sha256()

    # put the tx hash into sha256
    hash_func.update(tx_hash)

    # hash the tx all the way up to get the merkle root
    for h in hashes:
        hash_func.update(h)

    # check if the resulting hash equals the merkle root
    return hash_func.hexdigest() == merkle_root


def test():

    # test calculating maps of hashes required for SPV
    tree_map = [-1, 1, 1, -1]
    print(tree_map)

    hash_maps = calculate_hashes_map(tree_map)
    print(hash_maps)


if __name__ == "__main__":
    test()
