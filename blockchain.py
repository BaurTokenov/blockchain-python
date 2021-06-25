from block import Block


class Blockchain:
    """
    Blockchain: a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        last_block = self.chain[-1]
        new_block = Block.mine_block(last_block, data)
        self.chain.append(new_block)

    def __repr__(self):
        return f"Blockchain: {self.chain} "

    def print(self):
        for block in self.chain:
            print(block.data)
        print()


def main():
    blockchain = Blockchain()
    blockchain.add_block("one")
    blockchain.add_block("two")
    blockchain.add_block("three")
    blockchain.print()
    print(blockchain)

    print(f"blockchain.py __name__: {__name__}")


if __name__ == "__main__":
    main()
