from json import dumps, loads


class BlockHeader:

    def __init__(self, prev_hash, nonce, merkle_root, timestamp):
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.merkle_root = merkle_root
        self.timestamp = timestamp

    @property
    def to_string(self):
        """
        :return: a string representation of the block header with double quotes surround the key values.
        """
        return dumps(self.__dict__)


def header_from_string(s):
    """
    Create a Block Header object from a string representation of the header
    :param s: a string representation of the header
    :return: a block header object
    """
    return header_from_json(loads(s))


def header_from_json(j):
    """
    Create a block header from a json object
    :param j: a block header in json format
    :return: a block header object
    """
    return BlockHeader(j["prev_hash"], j["nonce"], j["merkle_root"], j["timestamp"])
