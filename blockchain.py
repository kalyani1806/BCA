import hashlib
import json
import time


def sha256(data):
    """Returns SHA-256 hash of input bytes."""
    return hashlib.sha256(data).hexdigest()

def hash_dict(obj):
    """Hash a dictionary by JSON-encoding it with sorted keys."""
    encoded = json.dumps(obj, sort_keys=True).encode()
    return sha256(encoded)

def merkle_root(transactions):
    """
    Computes Merkle Root from a list of transaction objects.
    Each transaction must have tx.id (already hashed).
    """
    if not transactions:
        return sha256(b"")

 
    layer = [tx.id for tx in transactions]

    while len(layer) > 1:
        new_layer = []
                for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if (i + 1) < len(layer) else left  # duplicate last if odd
            new_layer.append(sha256((left + right).encode()))
        layer = new_layer
    return layer[0]


class Block:
    def __init__(self, index, prev_hash, transactions, timestamp=None, nonce=0):
        self.index = index
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.timestamp = timestamp or int(time.time())
        self.nonce = nonce
        self.merkle_root = merkle_root(transactions)
        self.hash = None  # filled after mining

    
    def header(self):
        header_dict = {
            "index": self.index,
            "prev_hash": self.prev_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "merkle_root": self.merkle_root
        }
        return json.dumps(header_dict, sort_keys=True).encode()

    def compute_hash(self):
        """Computes the block hash using the header."""
        return sha256(self.header())



class Blockchain:
    def __init__(self):
        self.chain = []
        self.total_work = 0  # simple PoW counter for demo

        genesis = Block(0, "0" * 64, [])
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    def add_block(self, block):
        """Append a valid block to the chain."""
        self.chain.append(block)
        self.total_work += 1  

    def best_block(self):
        return self.chain[-1]

    @property
    def height(self):
        return len(self.chain)-1 
