import socket

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 65432))

# Send a message to the server
message = "Hello"
client_socket.sendall(message.encode())

# Receive the hash response from the server
data = client_socket.recv(1024).decode()
print(f"Server response: {data}")

# Extract the hash from the response
msg_hash = data.split("Hash: ")[1]

# Close the socket
client_socket.close()

# Reconnect to the server to retrieve the message using the hash
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 65432))

# Send the hash to retrieve the message
client_socket.sendall(f"HASH:{msg_hash}".encode())

# Receive and print the message
data = client_socket.recv(1024).decode()
print(f"Retrieved message: {data}")

# Close the socket
client_socket.close()
