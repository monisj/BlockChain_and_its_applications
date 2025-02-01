import socket
import json
from cryptography.fernet import Fernet

# Define your secret key
SECRET_KEY = Fernet.generate_key()  # Generate a key (do this once and reuse it in both client and server)
fernet = Fernet(SECRET_KEY)
print(SECRET_KEY)
# Database to store users' balances and messages
users_data = {
    "A": {"balance": 100, "messages": []},
    "B": {"balance": 100, "messages": []}
}

# Function to handle transactions and message passing
def handle_transaction(sender, receiver, message):
    if sender not in users_data or receiver not in users_data:
        return "Invalid users"

    if users_data[sender]["balance"] > 0:
        users_data[sender]["balance"] -= 1
        users_data[receiver]["balance"] += 1
        users_data[receiver]["messages"].append(f"From {sender}: {message}")
        return f"Transaction successful. Message sent to {receiver}."
    else:
        return "Insufficient balance"

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(2)

print("Server is listening on port 65432...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    # Receive encrypted data from the client
    encrypted_data = conn.recv(1024)
    print("Encrypted payload = ",encrypted_data)
    if not encrypted_data:
        break

    try:
        # Decrypt the payload
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        print("Decrypted Data=",decrypted_data)
        request = json.loads(decrypted_data)

        sender = request["sender"]
        receiver = request["receiver"]
        message = request["message"]
        # signature = request["sign"]

    

        # Handle the transaction and message passing
        # response = handle_transaction(sender, receiver, message)
    except Exception as e:
        response = f"Error processing request: {str(e)}"

    # Send response back to the client
    conn.sendall(response.encode())
    conn.close()
