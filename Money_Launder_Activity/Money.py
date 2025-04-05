import uuid
from datetime import datetime, timedelta

# Simulated Blockchain Ledger
ledger = []

# Wallets
wallets = {
    'Asif': str(uuid.uuid4()),
    'Ali': str(uuid.uuid4()),
    'Bilal': str(uuid.uuid4()),
    'Sajid': str(uuid.uuid4()),
    'Faiza': str(uuid.uuid4())
}

# Custom Asset
asset = {
    'name': 'PKRToken',
    'total_issued': 500000
}

# Smurfing deposits into Asif's wallet
smurf_amounts = [25000, 30000, 20000, 50000, 40000, 35000, 50000]  # Total = 250000
deposit_time = datetime.now()

for i, amt in enumerate(smurf_amounts):
    tx = {
        'txid': str(uuid.uuid4()),
        'timestamp': deposit_time + timedelta(minutes=i * 10),
        'from': 'external_source',
        'to': wallets['Asif'],
        'amount': amt,
        'asset': asset['name'],
        'type': 'deposit'
    }
    ledger.append(tx)

# Suspicious transfers to recipients
transfer_time = deposit_time + timedelta(hours=1)
recipients = ['Ali', 'Bilal', 'Sajid', 'Faiza']
alert_triggered = False
suspicious_tx = []

for i, recipient in enumerate(recipients):
    tx = {
        'txid': str(uuid.uuid4()),
        'timestamp': transfer_time + timedelta(minutes=i * 100),  # Staggered
        'from': wallets['Asif'],
        'to': wallets[recipient],
        'amount': 50001,
        'asset': asset['name'],
        'type': 'transfer'
    }
    ledger.append(tx)
    suspicious_tx.append(tx)

# --- Detect Suspicious Activity Based on Criteria ---
def check_suspicious(transactions):
    flags = []
    if len(transactions) > 3 and sum(tx['amount'] for tx in transactions) > 200000:
        for tx in transactions:
            if tx['amount'] > 50000:
                flags.append(tx)
    return flags

suspicious_flags = check_suspicious(suspicious_tx)

# --- Generate Alert ---
if suspicious_flags:
    alert_triggered = True
    print("🚨 RED FLAG ALERT: Suspicious activity detected from Asif's wallet 🚨")
    for tx in suspicious_flags:
        print(f"  - Sent {tx['amount']} {tx['asset']} to {tx['to']} at {tx['timestamp']}")
else:
    print("✅ No suspicious activity detected.")

# --- Audit Log Preview ---
print("\n📜 AUDIT TRAIL")
for tx in ledger:
    print(f"{tx['timestamp']} | {tx['type'].upper()} | From: {tx['from']} -> To: {tx['to']} | Amount: {tx['amount']} {tx['asset']}")
