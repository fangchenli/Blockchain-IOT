
from json import dumps


class BlockHeader:

    def __init__(self, prev_hash, nonce, merkle_root):
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.merkle_root = merkle_root

    @property
    def to_string(self):
        """
        :return: a string representation of the block header with double quotes surround the key values.
        """
        return dumps(self.__dict__)
