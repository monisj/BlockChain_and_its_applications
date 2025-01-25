import socket
import hashlib

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
host = '127.0.0.1'
port = 12345

# Connect to the server
client_socket.connect((host, port))
print(f"Connected to server at {host}:{port}")

# Hash the client's identity (As an example can be way more complicated)
identity = "A2"  # Change this to test different clients
hashed_identity = hashlib.sha256(identity.encode()).hexdigest()

# Send the hashed identity to the server
client_socket.send(hashed_identity.encode('utf-8'))

# Receive authorization status from the server
response = client_socket.recv(1024).decode('utf-8')
print(f"Server response: {response}")

if response == "Authorized":
    while True:
        # Send a message to the server
        message = input("Enter a message (or 'exit' to quit): ")
        client_socket.send(message.encode('utf-8'))

        if message.lower() == "exit":
            break

        # Receive confirmation from the server
        confirmation = client_socket.recv(1024).decode('utf-8')
        print(f"Server confirmation: {confirmation}")

    # Receive the client's messages from the server
    messages = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {messages}")
else:
    print("Unauthorized access.")

# Close the connection
client_socket.close()