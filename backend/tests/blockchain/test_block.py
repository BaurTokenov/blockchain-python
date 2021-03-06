import time
import pytest

from backend.config import MINE_RATE, SECONDS
from backend.blockchain.block import Block, GENESIS_DATA
from backend.util.hex_to_binary import hex_to_binary


def test_mine_block():
    last_block = Block.genesis()
    data = "test-data"
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)

    assert block.data == data

    assert block.last_hash == last_block.hash

    assert hex_to_binary(block.hash)[0 : block.difficulty] == "0" * block.difficulty


def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)

    assert genesis.timestamp == GENESIS_DATA["timestamp"]
    assert genesis.last_hash == GENESIS_DATA["last_hash"]
    assert genesis.hash == GENESIS_DATA["hash"]
    assert genesis.data == GENESIS_DATA["data"]

    for key, value in GENESIS_DATA.items():
        assert getattr(genesis, key) == value


def test_quickly_mined_block():
    last_block = Block.mine_block(Block.genesis(), "bauka")
    # why is the block considered to be mined pretty quickly
    mined_block = Block.mine_block(last_block, "bauyrzhan")
    # and why does the difficulty increase??
    # okay I guess usually it takes less than a second to mine a block with difficulty=3,
    # therefore the author assumed that this mining phase couldn't be more than 4 seconds.
    # still a weird assumption, I think.
    assert mined_block.difficulty == last_block.difficulty + 1


def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), "bauka")
    # artifically decrease the mining speed
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, "bauyrzhan")
    assert mined_block.difficulty == last_block.difficulty - 1


def test_mined_block_difficulty_limits_at_1():
    last_block = Block(time.time_ns(), "test_last_hash", "test_hash", "test_data", 1, 0)

    time.sleep(MINE_RATE / SECONDS)

    mined_block = Block.mine_block(last_block, "bauyrzhan")
    assert mined_block.difficulty == 1


@pytest.fixture
def last_block():
    return Block.genesis()


@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, "bauka_data")


def test_is_valid_block(last_block, block):
    Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_last_hash(last_block, block):
    block.last_hash = "hello world"

    with pytest.raises(Exception, match="The block last_hash must be correct"):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_proof_of_work(last_block, block):
    block.hash = "fff12123ff12f1"

    with pytest.raises(Exception, match="The proof of work requirement was not met"):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_jumped_difficulty(last_block, block):
    block.difficulty = last_block.difficulty + 5
    block.hash = f'{"0" * block.difficulty}111abc'

    with pytest.raises(Exception, match="The difficulty was adjusted by more than 1"):
        Block.is_valid_block(last_block, block)


def test_is_valid_block_bad_hash(last_block, block):
    block.hash = block.difficulty * "0" + "bababbcbcd"

    with pytest.raises(Exception, match="The block hash must be correct"):
        Block.is_valid_block(last_block, block)
