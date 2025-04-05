import uuid
import random
from datetime import datetime, timedelta

# Setup wallets
main_wallet = "Asif"
recipients = ["Ali", "Bilal", "Sajid", "Faiza"]
mixer_wallets = [f"mixer_{i}" for i in range(5)]  # temporary wallets
ledger = []

# Send Rs. 500000 to mixer wallets from Asif
asif_fund = 500000
per_mixer = asif_fund // len(mixer_wallets)
start_time = datetime.now()

for i, wallet in enumerate(mixer_wallets):
    tx = {
        "txid": str(uuid.uuid4()),
        "timestamp": start_time + timedelta(minutes=i * 3),
        "from": main_wallet,
        "to": wallet,
        "amount": per_mixer,
        "note": "Mixer deposit"
    }
    ledger.append(tx)

# Wait and redistribute from mixer wallets to final recipients
mix_time = start_time + timedelta(hours=1)

for wallet in mixer_wallets:
    # Pick 1-2 random recipients per wallet
    parts = random.sample(recipients, k=random.randint(1, 2))
    chunks = [random.randint(20000, 60000) for _ in parts]

    for recipient, chunk in zip(parts, chunks):
        tx = {
            "txid": str(uuid.uuid4()),
            "timestamp": mix_time + timedelta(minutes=random.randint(1, 60)),
            "from": wallet,
            "to": recipient,
            "amount": chunk,
            "note": "Mixer payout"
        }
        ledger.append(tx)

# Print result
print("🔄 Mixed Transactions (Simulated):\n")
for tx in ledger:
    print(f"{tx['timestamp']} | {tx['from']} ➝ {tx['to']} | {tx['amount']} PKR | {tx['note']}")
