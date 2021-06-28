import time
from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS

blockchain = Blockchain()

random_data = [
    "bauka",
    "bauyrzhan",
    "prekol",
    "kak dela",
    "kak tebya zovoot",
    "kak naiti",
    "nadandyktan arylu",
    "abay kunanbaev",
    "ybyrai altynsarin",
    "mukhtar magaueen",
]

avg_rate_sum = 0

for i in range(300):
    data = random_data[i % len(random_data)]
    blockchain.add_block(data)
    if i > 1:
        prev_block = blockchain.chain[i - 1]
        cur_block = blockchain.chain[i]
        cur_mine_rate = (cur_block.timestamp - prev_block.timestamp) / SECONDS
        avg_rate_sum += cur_mine_rate
        print(
            "Mining rate:",
            cur_mine_rate,
            "difficulty:",
            cur_block.difficulty,
            "avg_rate:",
            avg_rate_sum / (i - 1),
        )
