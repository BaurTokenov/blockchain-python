from backend.blockchain.block import Block, GENESIS_DATA


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

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate incoming chain.
        Enforce the following rules of the blockchain:
        - the chain must start with a genesis block
        - the blocks must be formatted correctly
        """
        first_block = chain[0]
        if first_block != Block.genesis():
            raise Exception("The first block is not the genesis block")

        for i in range(1, len(chain)):
            last_block = chain[i - 1]
            block = chain[i]
            Block.is_valid_block(last_block, block)


def main():
    blockchain = Blockchain()
    blockchain.add_block("one")
    blockchain.add_block("two")
    blockchain.add_block("three")
    blockchain.print()
    blockchain.chain[0] = blockchain.chain[-1]
    blockchain.chain[-1].last_hash = "adbfefabdf"
    Blockchain.is_valid_chain(blockchain.chain)
    print(blockchain)

    print(f"blockchain.py __name__: {__name__}")


if __name__ == "__main__":
    main()
