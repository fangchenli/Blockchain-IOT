from json import dumps
from hashlib import sha256
from Transaction import tx_from_string


class MerkleTreeNode:

    def __init__(self, tx=None, parent=None):
        self.depth = 0
        self.tx = tx
        self.hash = calculate_hash(self.tx) if self.tx else ""
        self.parent = parent
        self.left = None
        self.right = None

    @property
    def to_string(self):
        """
        :return: a string representation of the node with double quotes surround the key values.
        """
        return dumps(self.__dict__)

    @property
    def get_hash(self):
        """
        :return: the hash stored at this node
        """
        return self.hash

    @property
    def is_root(self):
        """
        :return: true if the node is the root
        """
        return not self.parent

    @property
    def is_leaf(self):
        """
        :return: true if the node is a leaf node
        """
        return not self.left & self.right

    @property
    def get_tx_string(self):
        """
        :return: the transaction in the node in string format
        """
        return self.tx

    @property
    def get_tx_object(self):
        """
        :return: the transaction in the node in object format
        """
        return tx_from_string(self.tx)


def calculate_hash(tx):
    """
    calculate the hash of the transaction
    :param tx: a string representation of a transaction
    :return: a hash value in string
    """
    # initialize sha256
    hash_func = sha256()

    # put the tx hash into sha256
    hash_func.update(tx)

    # return the hash of the
    return hash_func.hexdigest()
