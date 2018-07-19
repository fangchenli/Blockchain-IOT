import time
from json import dumps, loads


class Tx:
    """
    Transaction class
    """
    def __init__(self, type, sender, recipient, amount, message, timestamp=time.time()):
        """
        Initialize a transaction object
        :param type:
        :param sender:
        :param recipient:
        :param amount:
        :param message:
        """

        # Todo: finalize the transaction format

        self.type = type
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.message = message
        self.timestamp = timestamp

    @property
    def to_string(self):
        """
        :return: a string representation of the transaction with double quotes surround the key values.
        """
        return dumps(self.__dict__)


def tx_from_string(s):
    """
    Create a transaction object from a string.
    :param s: a string representation of a transaction.
    :return: a transaction object
    """

    # Todo: add input check, throw exceptions

    return tx_from_json(loads(s))


def tx_from_json(j):
    """
    Create a transaction from a json object.
    :param j: a transaction in json
    :return:
    """
    return Tx(j["type"], j["sender"], j["recipient"], j["amount"], j["message"], j["timestamp"])


"---------------------------------------------------------------------------------------------------------------------"


class TxDB:

    def __init__(self):
        self.in_uc = []  # unconfirmed incoming transactions
        self.in_co = []  # confirmed incoming transactions
        self.out_uc = []  # unconfirmed outgoing transactions
        self.out_co = []  # confirmed outgoing transactions

    def add_in_uc(self, tx):
        """
        add a transaction to unconfirmed incoming tx array
        :param tx:
        """
        self.in_uc.append(tx)

    def add_in_co(self, tx):
        """
        add a transaction to confirmed incoming tx array
        :param tx:
        """
        self.in_co.append(tx)

    def add_out_uc(self, tx):
        """
        add a transaction to unconfirmed outgoing tx array
        :param tx:
        """
        self.out_uc.append(tx)

    def add_out_co(self, tx):
        """
        add a transaction to confirmed outgoing tx array
        :param tx:
        """
        self.out_co.append(tx)

    def del_in_uc(self, tx):
        """
        delete a transaction from unconfirmed incoming tx array
        :param tx:
        """
        self.in_uc.remove(tx)

    def del_in_co(self, tx):
        """
         delete a transaction from confirmed incoming tx array
        :param tx:
        """
        self.in_co.remove(tx)

    def del_out_uc(self, tx):
        """
        delete a transaction from unconfirmed outgoing tx array
        :param tx:
        """
        self.out_uc.remove(tx)

    def del_out_co(self, tx):
        """
        delete a transaction from confirmed outgoing tx array
        :param tx:
        """
        self.out_co.remove(tx)


# test cases
def test():
    t1 = Tx('good', '1', '2', 100, 'hello world')

    print(t1.to_string)

    print(type(t1.to_string))

    j1 = loads(t1.to_string)

    print(type(j1))

    print(j1["type"])

    t2 = tx_from_json(j1)

    print(t2.to_string)

    t3 = tx_from_string(t1.to_string)

    print(t3.to_string)

    # Todo: test transaction database


if __name__ == "__main__":
    test()
