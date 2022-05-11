# Erik Fogle
# Date: 04/25/2022
# Description: Minimum-Viable-Product representing my blockchain microservices platform.

import hashlib
import json
from time import time


class ECoin(object):
    """
    Blockchain class that represents the connection of blocks to each other on the microservices platform.
    """

    def __init__(self):
        self._chain = list()
        self._transactions = list()
        self._nodes = set()
        # Creates initial block of the chain
        self.new_block(previous_hash=1, proof=100)

    def get_chain(self) -> list:
        """
        Getter that returns the entire blockchain.

        :return: (list) List containing the entire chain of blocks that have been mined.
        """
        return self._chain

    def new_block(self, proof: int, previous_hash=None) -> object:
        """
        Creates a new block and adds it to the chain.

        :param previous_hash: (str) Hash address of previous block.
        :param proof: (int) Proof given by proof of work algorithm.

        :return new_block: (obj) Newly created block.
        """

        new_block = {
            'index': len(self._chain) + 1,
            'proof': proof,
            'timestamp': time(),
            'previous_hash': previous_hash or self.hash(self._chain[-1]),
            'transactions': self._transactions
        }

        self._transactions = list()
        self._chain.append(new_block)
        return new_block

    def new_transaction(self, sender: str, amount: int, recipient: str) -> object:
        """
        Adds a new transaction to the list of transactions to the current block to be mined.

        :param sender: (str) Sender address.
        :param amount: (int) Amount of coin to send.
        :param recipient: (str) Recipient address .

        :return: (int) Index of the current block to be mined.
        """

        self._transactions.append({
            'amount': amount,
            'recipient': recipient,
            'sender': sender
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self) -> object:
        """
        Returns the last block in the chain.

        :return: Last block currently in the chain
        """
        return self._chain[-1]

    @staticmethod
    def hash(block):
        """
        Generates an SHA-256 hash of a block

        :param block: (obj) block object being hashed
        :return: (str)
        """

        # ensure block is ordered for consistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof: int) -> int:
        """
        Basic proof of work algorithm:
            Finds a number x' such that hash(xx') contains 3 leading zeros.
            Where x is the previous proof, and x' is the new proof.
            Note: modifying the number of leading zeroes increases/decreases
                    the computational effort and time significantly with each
                    addition/removal of a zero respectively.

        :param last_proof: (int) Previous proof's int value.
        :return: (int)
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:
        """
        Validates the proof i.e. if calling hash(last_proof, proof) contain 5 leading zeroes.

        :param last_proof: (int) Previous proof
        :param proof: (int) Current proof
        :return: (bool) True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:5] == '000'


def main() -> None:
    pass


if __name__ == '__main__':
    main()
