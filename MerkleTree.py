# package function import
from random import shuffle
from math import log2

# util function import
from Utils import calculate_hash


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

    def set_parent(self, parent):
        self.parent = parent


"---------------------------------------------------------------------------------------------------------------------"


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
        shuffle(tx_list_copy)  # shuffle the transactions

        # start building the tree from the transactions
        nodes = []
        for i in range(tree_height):
            # for the transaction layer
            if i == 0:
                j = 0
                while j < list_length:
                    tx_string = tx_list_copy.pop()  # pop one transaction from the list
                    curr_hash = calculate_hash(tx_string)  # calculate hash
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
                    node_left = nodes_copy.pop()
                    node_right = nodes_copy.pop()

                    # hash the two nodes together
                    curr_hash = calculate_hash(node_left.hash + node_right.hash)

                    # using the hash to create a new node, add to array
                    nodes.append(MerkleTreeNode(curr_hash, tree_height - i, node_left, node_right))

                    # set the parent of the two children nodes
                    node_left.set_parent(nodes[-1])
                    node_right.set_parent(nodes[-1])
                    j += 1

        # final step, calculate the root hash
        if len(nodes) == 2:

            # pop two nodes
            node_left = nodes.pop()
            node_right = nodes.pop()

            # calculate their hash
            root_hash = calculate_hash(node_left.hash + node_right.hash)

            # create the root node
            self.root = MerkleTreeNode(root_hash, left=node_left, right=node_right)
        else:
            # raise runtime error, this is very unlikely to happen
            raise RuntimeError("Error occurred during merkle tree building process. Hashes didn't converge to one root")

    @property
    def get_root(self):
        return self.root


"---------------------------------------------------------------------------------------------------------------------"


# test cases
def test():
    # test generator
    xl = [2 ** i for i in range(10)]
    # print(xl)

    # test the smallest element in a list that meet certain condition
    f = 8
    re = next(n for n in xl if n >= f)
    # print(re)
    # print(int(log2(re)))

    # test the merkle tree
    tx_list = ['123', '456', '789',
               'abc', 'def', 'ghi',
               'jkl', 'mno', 'pqr']

    tree = MerkleTree(tx_list)

    print(tree.get_root.depth)

    print(tree.get_root.left.hash)


if __name__ == "__main__":
    test()
