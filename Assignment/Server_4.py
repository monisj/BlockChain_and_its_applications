import socket
import hashlib

# Predefined list of authorized hashed identities (e.g., hashed usernames)
authorized_identities = {
    hashlib.sha256("A1".encode()).hexdigest(),
    hashlib.sha256("A2".encode()).hexdigest(),
    hashlib.sha256("A3".encode()).hexdigest(),
}

# Dictionary to store linked lists for each client
client_data = {}

# Linked list node
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Linked list class
class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def display(self):
        messages = []
        current = self.head
        while current:
            messages.append(current.data)
            current = current.next
        return messages

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
host = '127.0.0.1'
port = 12345

# Bind the socket to the address and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)
print(f"Server listening on {host}:{port}...")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    # Receive the hashed identity from the client
    hashed_identity = client_socket.recv(1024).decode('utf-8')
    print(f"Received hashed identity: {hashed_identity}")

    # Verify the hashed identity
    if hashed_identity in authorized_identities:
        print("Client authorized.")
        client_socket.send("Authorized".encode('utf-8'))

        # Initialize a linked list for the client if it doesn't exist
        if hashed_identity not in client_data:
            client_data[hashed_identity] = LinkedList()

        while True:
            # Receive a message from the client
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() == "exit":
                break

            # Append the message to the client's linked list
            client_data[hashed_identity].append(message)
            print(f"Stored message for {hashed_identity}: {message}")
            
            # Send a confirmation to the client
            client_socket.send("Message stored successfully.".encode('utf-8'))

        # Send the client's messages back
        messages = client_data[hashed_identity].display()
        client_socket.send(f"Your messages: {messages}".encode('utf-8'))
    else:
        print("Client not authorized.") #just as a test if unknown user enters the systems
        client_socket.send("Unauthorized".encode('utf-8'))

    # Close the connection
    client_socket.close()
    print("Dictornay=",client_data)
