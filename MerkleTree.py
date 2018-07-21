# package function import
from math import log2
from hashlib import sha256


class MerkleTreeNode:

    def __init__(self, h, depth=0, left=None, right=None):
        """
        Initialize a merkle tree node
        :param h: hash value stored in this node
        :param depth: the depth of the node, 0 for the root node
        :param left: left node
        :param right:  right node
        """
        self.depth = depth
        self.hash = h
        self.parent = None
        self.left = left
        self.right = right

    def is_root(self):
        """
        :return: true if the node is the root
        """
        return self.parent is None

    def has_left(self):
        return self.left is not None

    def has_right(self):
        return self.right is not None

    @property
    def is_leaf(self):
        """
        :return: true if the node is a leaf node
        """
        return self.has_left() and self.has_right()

    def set_parent(self, parent):
        self.parent = parent


"---------------------------------------------------------------------------------------------------------------------"


# noinspection PyTypeChecker
class MerkleTree:

    def __init__(self, tx_list):
        """
        Initialize a merkle tree.
        :param tx_list: a list of transactions in string format
        """
        self.tx_list = tx_list
        self.root = ''
        self.build_tree()

    def build_tree(self):
        """
        Build the merkle tree from the transaction list.
        """
        list_length = len(self.tx_list)
        tx_list_copy = self.tx_list.copy()

        # calculate the required number of leaf nodes
        leaf_number = next(n for n in [2 ** i for i in range(10)] if n >= list_length)

        tree_height = int(log2(leaf_number))  # calculate the height of the tree
        # shuffle(tx_list_copy)  # shuffle the transactions

        # start building the tree from the transactions
        nodes = []
        for i in range(tree_height):
            # for the transaction layer
            if i == 0:
                j = 0
                while j < list_length:
                    tx_string = tx_list_copy.pop(0)  # pop one transaction from the list
                    curr_hash = self.calculate_hash(tx_string)  # calculate hash
                    nodes.append(MerkleTreeNode(curr_hash, tree_height - i))  # create the node and add to node array

                    # for first (leaf_number - list_length) transactions, add another copy of each tx to the node array
                    if j < leaf_number - list_length:
                        nodes.append(MerkleTreeNode(curr_hash, tree_height - i))

                    j += 1

            # for non transaction layer
            else:
                nodes_copy = nodes.copy()  # copy hashes from previous layer
                nodes_length = len(nodes)
                nodes.clear()  # clear the node array

                # hash hashes in pair of 2
                j = 0
                while j < nodes_length / 2:
                    # pop 2 nodes from the node array
                    node_left = nodes_copy.pop(0)
                    node_right = nodes_copy.pop(0)

                    # hash the two nodes together
                    curr_hash = self.calculate_hash(node_left.hash + node_right.hash)

                    # using the hash to create a new node, add to array
                    nodes.append(MerkleTreeNode(curr_hash, tree_height - i, node_left, node_right))

                    # set the parent of the two children nodes
                    node_left.set_parent(nodes[-1])
                    node_right.set_parent(nodes[-1])
                    j += 1

            # print out the tree
            # for node in nodes:
            #     print(node.hash)
            # print('\n--')

        # final step, calculate the root hash
        if len(nodes) == 2:

            # pop two nodes from the beginning of the list
            node_left = nodes.pop(0)
            node_right = nodes.pop(0)

            # calculate their hash
            root_hash = self.calculate_hash(node_left.hash + node_right.hash)

            # create the root node
            self.root = MerkleTreeNode(root_hash, left=node_left, right=node_right)
        else:
            # raise runtime error, this is very unlikely to happen
            raise RuntimeError("Error occurred during merkle tree building process. Hashes didn't converge to one root")

    def find_tx_path(self, tx_hash):
        """
        traverse the tree to find a tx
        :param tx_hash:
        :return: the path of a tx
        """
        # find the path recursively
        path = self.__find_tx_path_recursive(self.root, tx_hash)

        # if the tx is found, remove the ending 0 from the path
        if len(path) > 0:
            path.pop()
        return path

    def __find_tx_path_recursive(self, root, tx_hash):
        """
        a private recursive method that traverse the tree to find the path of a tx
        :param root:
        :param tx_hash: hash value of a tx
        :return: empty list if the tx hash is not in the tree
        """
        if root is None:
            return []
        if root.hash == tx_hash:
            return [0]
        res = self.__find_tx_path_recursive(root.left, tx_hash)
        if res:
            return [-1] + res
        res = self.__find_tx_path_recursive(root.right, tx_hash)
        if res:
            return [1] + res
        return []

    def find_node_from_path(self, path):
        """
        find a node from a path
        :param path: a list that indicate the path of a node, like [1, -1, -1, 1]
        :return: the merkle tree node
        """
        node = self.root
        for direction in path:
            if direction == -1:
                node = node.left
            elif direction == 1:
                node = node.right
            else:
                raise RuntimeError('Input path incorrect.')
        return node

    def find_hashes_for_confirmation(self, tx_path):
        """
        find all hashes required to verify a tx at given path
        :param tx_path: the path of the tx we want to verify
        :return: hashes
        """
        paths = self.calculate_hash_paths(tx_path)
        hashes = []
        for path in paths:
            print(path)
            node = self.find_node_from_path(path)
            hashes.append(node.hash)
        return hashes

    @staticmethod
    def calculate_hash_paths(path):
        """
        Given a merkle tree map of a transaction, calculate the corresponding maps to the required transactions
        in the merkle tree for SPV.
        :param path:
        """
        depth = len(path)
        maps = []
        i = depth
        while i > 0:
            # for transaction at higher level, remove the last element of the tree map
            if i < depth:
                del path[-1]

            # reverse one step of the map to get the complimentary transaction
            path[-1] *= -1

            # add to the 2-d array that stores the maps
            maps.append(path.copy())

            # move counter
            i -= 1
        return maps

    @staticmethod
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

    @staticmethod
    def confirm_tx(tx_hash, tx_path, merkle_root, hashes):
        """
        Confirm if a transaction is in one block
        :param tx_hash: hash of the tx
        :param tx_path: path of the tx
        :param merkle_root: the merkle root in a header of the block
        :param hashes: the corresponding tx hashes given by the full node
        :return: true if the tx exist under given merkle root and hashes
        """
        tx_path.reverse()  # reverse the path

        txhs = tx_hash
        # hash the tx all the way up to get the merkle root
        for i, h in enumerate(hashes):
            if tx_path[i] == -1:
                txhs = MerkleTree.calculate_hash(txhs + h)
            else:
                txhs = MerkleTree.calculate_hash(h + txhs)

        # check if the resulting hash equals the merkle root
        return txhs == merkle_root.hash


"---------------------------------------------------------------------------------------------------------------------"


# test cases
# noinspection PyTypeChecker
def test():

    # test the merkle tree
    tx_list = ['123', '456', '789',
               'abc', 'def', 'ghi',
               'jkl', 'mno', 'pqr']

    tree = MerkleTree(tx_list)

    print('-----------------------------------------------------------------------------------------------------------')

    ha = tree.calculate_hash('mno')

    print('\ntx hash: ')
    print(ha)

    path = tree.find_tx_path(ha)

    print('\ntx path: ')
    print(path)

    print('\nMerkle proof node paths: ')
    s = tree.find_hashes_for_confirmation(path.copy())
    print('\nMerkle proof node hashes: ')
    print(s)

    print('\nMerkle root: ')
    # print(tree.root.hash)

    # noinspection PyTypeChecker
    print(tree.confirm_tx(ha, path, tree.root, s))


if __name__ == "__main__":
    test()
