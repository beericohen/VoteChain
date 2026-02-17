import json
import os
import time
from .crypto_logic import CryptoManager

DATA_DIR = "data"
KEYS_DIR = os.path.join(DATA_DIR, "keys")
CHAIN_FILE = os.path.join(DATA_DIR, "blockchain.json")
VOTERS_FILE = os.path.join(DATA_DIR, "voters_status.json") # קובץ חדש למעקב

class BlockchainManager:
    """
    Manages the file-based blockchain, key storage, and voter tracking.
    """
    
    def __init__(self):
        self._ensure_directories()
        if not os.path.exists(CHAIN_FILE):
            self.init_chain()
        if not os.path.exists(VOTERS_FILE):
            self._init_voters_file()

    def _ensure_directories(self):
        os.makedirs(KEYS_DIR, exist_ok=True)

    def _init_voters_file(self):
        """Creates an empty list for tracking who voted."""
        with open(VOTERS_FILE, "w") as f:
            json.dump([], f)

    def init_chain(self):
        """Initializes an empty blockchain and resets voter list."""
        genesis_block = {
            "index": 0,
            "timestamp": time.time(),
            "vote": "GENESIS",
            "previous_hash": "0",
            "hash": CryptoManager.get_hash("GENESIS")
        }
        with open(CHAIN_FILE, "w") as f:
            json.dump([genesis_block], f, indent=4)
        
        # Reset voters list when chain is reset
        self._init_voters_file()

    def has_voted(self, public_key_pem):
        """Checks if a specific public key has already voted."""
        # We hash the public key to store it efficiently and consistently
        voter_id = CryptoManager.get_hash(public_key_pem)
        
        with open(VOTERS_FILE, "r") as f:
            voters = json.load(f)
            
        return voter_id in voters

    def mark_as_voted(self, public_key_pem):
        """Marks a voter as having voted."""
        voter_id = CryptoManager.get_hash(public_key_pem)
        
        with open(VOTERS_FILE, "r") as f:
            voters = json.load(f)
        
        if voter_id not in voters:
            voters.append(voter_id)
            with open(VOTERS_FILE, "w") as f:
                json.dump(voters, f, indent=4)

    def add_vote(self, vote_data):
        """Adds a new block to the chain."""
        chain = self.get_chain()
        last_block = chain[-1]
        
        new_block = {
            "index": len(chain),
            "timestamp": time.time(),
            "vote": vote_data,
            "previous_hash": last_block["hash"],
            "hash": "" 
        }
        
        block_content = json.dumps(new_block, sort_keys=True)
        new_block["hash"] = CryptoManager.get_hash(block_content)
        
        chain.append(new_block)
        
        with open(CHAIN_FILE, "w") as f:
            json.dump(chain, f, indent=4)
            
        return new_block["hash"]

    def get_chain(self):
        if not os.path.exists(CHAIN_FILE):
            self.init_chain()
        with open(CHAIN_FILE, "r") as f:
            return json.load(f)

    def save_key(self, name, key_data, is_private=False):
        suffix = "_priv.pem" if is_private else "_pub.pem"
        path = os.path.join(KEYS_DIR, f"{name}{suffix}")
        with open(path, "wb") as f:
            f.write(key_data)
        return path