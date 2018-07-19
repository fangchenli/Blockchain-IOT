from hashlib import sha256


def calculate_hash(tx):
    """
    calculate the hash of the transaction
    :param tx: a string representation of a transaction
    :return: a hash value in string
    """
    # initialize sha256
    hash_func = sha256()

    # put the tx hash into sha256
    hash_func.update(tx.encode('utf-8'))

    # return the hash of the
    return hash_func.hexdigest()


# prototype, not in use
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


# prototype, not in use
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

