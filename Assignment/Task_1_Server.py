import socket
import json
import hashlib

# Store the linked list and hash map on the server
linked_list = {"head": None}
Hash = {}

# Function to add a new element to the linked list
def add_element(new_data):
    data_hash = hashlib.sha256(new_data.encode()).hexdigest()
    Hash[data_hash] = new_data

    prev = None
    new_node = {"previous": prev, "data": data_hash, "next": None}
    if linked_list["head"] is None:  # If the list is empty
        linked_list["head"] = new_node
    else:
        current_node = linked_list["head"]
        while current_node["next"] is not None:
            current_node = current_node["next"]
        current_node["next"] = new_node
        new_node["previous"] = current_node

    return data_hash

# Function to retrieve the message using the hash
def get_message(data_hash):
    if data_hash in Hash:
        return Hash[data_hash]
    return "Message not found"

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1)

print("Server is listening on port 65432...")

while True:
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    # Receive message from the client
    data = conn.recv(1024).decode()
    if not data:
        break

    # Check if the client sent a hash or a new message
    if data.startswith("HASH:"):
        hash_value = data.split("HASH:")[1]
        message = get_message(hash_value)
        conn.sendall(message.encode())
    else:
        # Add the new message and get the hash
        msg_hash = add_element(data)
        conn.sendall(f"Message received and stored. Hash: {msg_hash}".encode())

    conn.close()
