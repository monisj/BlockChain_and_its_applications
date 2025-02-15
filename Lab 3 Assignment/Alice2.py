import threading
import time
import hashlib
import random

# Global ledger (shared among all servers)
ledger = []

# Difficulty level for PoW (adjustable)
DIFFICULTY = 4  # Number of leading zeros in hash

# Lock for synchronizing ledger access
ledger_lock = threading.Lock()

# Event to signal that a block has been mined
block_mined_event = threading.Event()
verified_nonce = None
verified_hash = None

class BlockchainServer(threading.Thread):
    def __init__(self, server_id, transactions, all_servers,val):
        super().__init__()
        self.server_id = server_id
        self.transactions = transactions
        self.all_servers = all_servers
        self.val=val
    
    def run(self):
        global verified_nonce, verified_hash
        start_time = time.time()
        time.sleep(self.val)  # Simulating network delay
        nonce, hash_result = self.proof_of_work(self.transactions)
        end_time = time.time()
        computational_time = end_time - start_time
        
        with ledger_lock:
            if not block_mined_event.is_set():  # First server to mine the block
                block_mined_event.set()
                verified_nonce = nonce
                verified_hash = hash_result
                print(f"Server {self.server_id} won! Computed hash {hash_result} in {computational_time:.4f} sec")
                print(f"Server {self.server_id} Start time = {start_time}")
                print(f"Server  {self.server_id} Server end time = {end_time}\n\n")
                
                # Broadcast the mined block to other servers for verification
                self.verify_with_other_servers()
    
    def proof_of_work(self, transactions):
        nonce = 0
        while not block_mined_event.is_set():
            block_data = f"{transactions}{nonce}".encode()
            block_hash = hashlib.sha256(block_data).hexdigest()
            if block_hash.startswith('0' * DIFFICULTY):
                return nonce, block_hash
            nonce += 1
        return None, None  # If another server wins, exit
    
    def verify_with_other_servers(self):
        global verified_nonce, verified_hash
        valid = all(self.verify_block(verified_nonce, verified_hash) for server in self.all_servers if server.server_id != self.server_id)
        
        if valid:
            
                ledger.append({
                    "server_id": self.server_id,
                    "transactions": self.transactions,
                    "nonce": verified_nonce,
                    "hash": verified_hash
                })
                print(f"Block verified and added to ledger by Server {self.server_id}.")
                print(f"Server Transaction {transaction_data}.")
                print(f"Server nonce {verified_nonce}.")
                print(f"Server Hash {verified_hash}")
        else:
            print("Block verification failed.")
    
    def verify_block(self, nonce, hash_result):
        block_data = f"{self.transactions}{nonce}".encode()
        print(block_data)
        return hashlib.sha256(block_data).hexdigest() == hash_result

# Simulate multiple servers handling a transaction
num_servers = 3
transaction_data = "Shehbaz"
delay = 2
servers = [BlockchainServer(i, transaction_data, None,delay+i+5) for i in range(num_servers)]
for server in servers:
    server.all_servers = servers if servers else []  # Assign the full list of servers

for server in servers:
    server.start()

for server in servers:
    server.join()

# Display the final ledger
print("\nFinal Ledger:")
for entry in ledger:
    print(entry)
