import threading
import time
import hashlib
import random

# Global ledger (shared among all servers)
ledger = []

# Difficulty level for PoW (adjustable)
DIFFICULTY = 4 # Number of leading zeros in hash

# Lock for synchronizing ledger access
ledger_lock = threading.Lock()

class BlockchainServer(threading.Thread):
    def __init__(self, server_id, transactions,val):
        super().__init__()
        self.server_id = server_id
        self.transactions = transactions
        self.val=val
    
    def run(self):
        time.sleep(self.val)  # Simulating network delay
        start_time = time.time()
        nonce, hash_result = self.proof_of_work(self.transactions)
        end_time = time.time()
        computational_time = end_time - start_time
        
        with ledger_lock:
            if nonce is not None:
                ledger.append({
                    "server_id": self.server_id,
                    "transactions": self.transactions,
                    "nonce": nonce,
                    "hash": hash_result,
                    "start_time": start_time,
                    "end_time": end_time,
                    "computational_time": computational_time
                })
                print(f"Server {self.server_id} won! Computed hash {hash_result} in {computational_time:.4f} sec")
                print(f"Server {self.server_id} Start time = {start_time}")
                print(f"Server  {self.server_id} Server end time = {end_time}\n\n")
    def proof_of_work(self, transactions):
        nonce = 0
        while True:
            block_data = f"{transactions}{nonce}".encode()
            block_hash = hashlib.sha256(block_data).hexdigest()
            if block_hash.startswith('0' * DIFFICULTY):
                return nonce, block_hash
            nonce += 1
            if nonce % 100000 == 0:  # Prevent infinite loops in case of errors
                return None, None

# Simulate multiple servers handling a transaction
num_servers = 3  
transaction_data = "Shehbaz"
delay=10
servers = [BlockchainServer(i, transaction_data,delay+i+1) for i in range(num_servers)]

for server in servers:
    server.start()

for server in servers:
    server.join()

# Display the final ledger
print("\nFinal Ledger:")
for entry in ledger:
    print(entry)
