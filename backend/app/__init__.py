import os
import random
import requests
from flask import Flask, jsonify, request

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub(blockchain=blockchain)


@app.route("/")
def route_default():
    return "Welcome to the Blockchain"


@app.route("/blockchain")
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route("/blockchain/mine")
def route_blockchain_mine():
    transaction_data = "stubbed_transaction_data"

    blockchain.add_block(transaction_data)
    new_block = blockchain.chain[-1]

    pubsub.broadcast_block(new_block)

    return jsonify(new_block.to_json())


ROOT_PORT = 7000
PORT = ROOT_PORT

if os.environ.get("PEER") == "True":
    PORT = random.randint(PORT + 1, 8000)

    result = requests.get(f"http://localhost:{ROOT_PORT}/blockchain")

    result_blockchain = Blockchain.from_json(result.json())
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print("\n -- Successfully synchronized the local chain")
    except Exception as e:
        print(f"\n -- Error synchronizing: {e}")


app.run(port=PORT)