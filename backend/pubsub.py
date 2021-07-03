import time
import os

from dotenv import load_dotenv
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block
from backend.blockchain.blockchain import Blockchain

load_dotenv()

pnconfig = PNConfiguration()
pnconfig.subscribe_key = os.environ.get("SUBSCRIBE_KEY")
pnconfig.publish_key = os.environ.get("PUBLISH_KEY")
pubnub = PubNub(pnconfig)


CHANNELS = {"TEST": "TEST", "BLOCK": "BLOCK"}


class Listener(SubscribeCallback):
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        print(
            f"channel: {message_object.channel} | message_object: {message_object.message}"
        )
        if message_object.channel == CHANNELS["BLOCK"]:
            block_json = message_object.message
            block = Block.from_json(block_json=block_json)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print("\n -- Successfully replaced the local chain.")
            except Exception as e:
                print(f"\n -- Did not replace chain: {e}")

        # return super().message(pubnub, message)


class PubSub:
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between the nodes of the blockchain network.
    """

    def __init__(self, blockchain):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        """
        Publish the message object to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block: Block):
        """
        Broadcast a block object to all nodes.
        """
        self.publish(CHANNELS["BLOCK"], block.to_json())


def main():
    time.sleep(1)


if __name__ == "__main__":
    main()
