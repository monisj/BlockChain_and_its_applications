class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

class SecureLedger:
    def __init__(self):
        self.balances = {}

    def create_account(self, user, balance):
        self.balances[user] = balance

    def process_transaction(self, transaction):
        # Validate that the sender has enough balance
        if transaction.sender not in self.balances:
            self.balances[transaction.sender] = 0  # Ensure sender account exists
        if transaction.recipient not in self.balances:
            self.balances[transaction.recipient] = 0  # Ensure recipient account exists

        if self.balances[transaction.sender] >= transaction.amount:
            self.balances[transaction.sender] -= transaction.amount
            self.balances[transaction.recipient] += transaction.amount
            print(f"Transaction processed: {transaction.sender} → {transaction.recipient}: {transaction.amount} coins")
        else:
            print(f"Transaction rejected: {transaction.sender} does not have enough balance.")

    def get_balance(self, user):
        return self.balances.get(user, 0)

# Demonstration
secure_ledger = SecureLedger()
secure_ledger.create_account("Alice", 50)

# Alice sends 50 coins to Bob
secure_ledger.process_transaction(Transaction("Alice", "Bob", 50))

# Alice tries to send 50 coins to Linus (but has no coins left)
secure_ledger.process_transaction(Transaction("Alice", "Linus", 50))

# Display balances
print("\nBalances with validation:")
print(f"Alice: {secure_ledger.get_balance('Alice')} coins")
print(f"Bob: {secure_ledger.get_balance('Bob')} coins")
print(f"Linus: {secure_ledger.get_balance('Linus')} coins")
