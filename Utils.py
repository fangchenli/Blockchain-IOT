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
