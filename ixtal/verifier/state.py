# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# Copyright © 2023 philanthrope <-- main author
# Copyright © 2024 Manifold Labs

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import threading
import bittensor as bt

from loguru import logger
from substrateinterface import SubstrateInterface

class SimpleBlockSubscriber:
    '''
    Simple block subscriber for the substrate blockchain.

    Args:
        substrate_url (str): The URL of the substrate node.
    '''
    def __init__(self, substrate_url):
        self.substrate = SubstrateInterface(
            ss58_format=bt.__ss58_format__,
            use_remote_preset=True,
            url=substrate_url,
            type_registry=bt.__type_registry__,
        )

    def block_subscription_handler(self, obj, update_nr, subscription_id):
        block_number = obj['header']['number']
        print(f"Received block number: {block_number}")

    def start_subscription(self):
        self.substrate.subscribe_block_headers(self.block_subscription_handler)

    def run_in_thread(self):
        subscription_thread = threading.Thread(target=self.start_subscription, daemon=True)
        subscription_thread.start()
        print("Block subscription started in background thread.")


def log_event(self, event):
    # Log event
    if not self.config.neuron.dont_save_events:
        logger.log("EVENTS", "events", **event.__dict__)
