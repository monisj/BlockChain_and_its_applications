import json
from datetime import datetime

class SimpleLedger:
    def __init__(self, filename="blockchain_log.json"):
        self.filename = filename
        try:
            with open(filename, "r") as f:
                self.chain = json.load(f)
        except:
            self.chain = []

    def log_contribution(self, node_id, accuracy, tokens_awarded):
        entry = {
            "timestamp": str(datetime.utcnow()),
            "node": node_id,
            "accuracy": round(accuracy, 4),
            "tokens": tokens_awarded
        }
        self.chain.append(entry)
        with open(self.filename, "w") as f:
            json.dump(self.chain, f, indent=2)
        print(f"✔️ Logged: {entry}")

# Example
if __name__ == "__main__":
    ledger = SimpleLedger()
    ledger.log_contribution("booth-1", accuracy=0.91, tokens_awarded=12)
    ledger.log_contribution("booth-2", accuracy=0.81, tokens_awarded=2)
    ledger.log_contribution("booth-3", accuracy=0.71, tokens_awarded=32)
    ledger.log_contribution("booth-4", accuracy=0.61, tokens_awarded=22)
    ledger.log_contribution("booth-5", accuracy=0.51, tokens_awarded=2)
    ledger.log_contribution("booth-6", accuracy=0.41, tokens_awarded=1)
