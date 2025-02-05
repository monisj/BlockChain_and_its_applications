class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

class SimpleLedger:
    def __init__(self):
        self.balances = {}

    def create_account(self, user, balance):
        self.balances[user] = balance

    def process_transaction(self, transaction):
        # No validation of balance, allowing double spending
        if transaction.sender not in self.balances:
            self.balances[transaction.sender] = 0  # Ensure sender account exists
        if transaction.recipient not in self.balances:
            self.balances[transaction.recipient] = 0  # Ensure recipient account exists
        
        self.balances[transaction.sender] -= transaction.amount
        self.balances[transaction.recipient] += transaction.amount

    def get_balance(self, user):
        return self.balances.get(user, 0)

# Demonstration
ledger = SimpleLedger()
ledger.create_account("Alice", 50)

# Alice sends 50 coins to Bob
ledger.process_transaction(Transaction("Alice", "Bob", 50))

# Alice sends 50 coins to Linus (double spend, no validation)
ledger.process_transaction(Transaction("Alice", "Linus", 50))

# Display balances
print("Balances without validation:")
print(f"Alice: {ledger.get_balance('Alice')} coins")
print(f"Bob: {ledger.get_balance('Bob')} coins")
print(f"Linus: {ledger.get_balance('Linus')} coins")
