import hashlib
import json
import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.messages = []
        self.peers = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        threading.Thread(target=self.listen_for_peers, daemon=True).start()
    
    def add_peer(self, peer_host, peer_port):
        self.peers.append((peer_host, peer_port))
    
    def listen_for_peers(self):
        while True:
            conn, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_peer, args=(conn,), daemon=True).start()
    
    def handle_peer(self, conn):
        data = conn.recv(1024)
        if data:
            message_data = json.loads(data.decode())
            if "message" in message_data and "hash" in message_data:
                self.store_message(message_data)
        conn.close()
    
    def receive_message(self, message):
        message_hash = self.generate_hash(message)
        message_data = {"message": message, "hash": message_hash}
        self.messages.append(message_data)
        self.distribute_message(message_data)
    
    def distribute_message(self, message_data):
        for peer_host, peer_port in self.peers:
            self.send_message_to_peer(peer_host, peer_port, message_data)
    
    def send_message_to_peer(self, host, port, message_data):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((host, port))
            peer_socket.send(json.dumps(message_data).encode())
            peer_socket.close()
        except Exception as e:
            print(f"Error sending message to {host}:{port} - {e}")
    
    def store_message(self, message_data):
        if "message" in message_data and "hash" in message_data:
            self.messages.append(message_data)
    
    def generate_hash(self, message):
        return hashlib.sha256(message.encode()).hexdigest()
    
    def verify_consensus(self):
        all_hashes = [set(self.get_hashes())]
        for peer_host, peer_port in self.peers:
            try:
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer_socket.connect((peer_host, peer_port))
                peer_socket.send(json.dumps({"request": "hashes"}).encode())
                peer_socket.close()
            except Exception as e:
                print(f"Error contacting peer {peer_host}:{peer_port} - {e}")
        consensus = all(hash_set == all_hashes[0] for hash_set in all_hashes)
        return consensus
    
    def get_hashes(self):
        return [msg.get("hash", "") for msg in self.messages if isinstance(msg, dict)]
    
    def print_messages(self):
        print(f"Server {self.host}:{self.port} Messages:")
        print(json.dumps(self.messages, indent=4))
    
    def print_hashes(self):
        print(f"Server {self.host}:{self.port} Hashes:")
        for msg in self.messages:
            print(msg.get("hash", ""))

class Client:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
    
    def send_message(self, message):
        print(f"Client sending: {message}")
        try:
            message_hash = hashlib.sha256(message.encode()).hexdigest()
            message_data = {"message": message, "hash": message_hash}
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.server_host, self.server_port))
            client_socket.send(json.dumps(message_data).encode())
            client_socket.close()
        except Exception as e:
            print(f"Error sending message to server: {e}")

# Initialize servers
server1 = Server("127.0.0.1", 5001)
server2 = Server("127.0.0.1", 5002)
server3 = Server("127.0.0.1", 5003)

# Establish peer connections
server1.add_peer("127.0.0.1", 5002)
server1.add_peer("127.0.0.1", 5003)
server2.add_peer("127.0.0.1", 5001)
server2.add_peer("127.0.0.1", 5003)
server3.add_peer("127.0.0.1", 5001)
server3.add_peer("127.0.0.1", 5002)

# Initialize clients
client1 = Client("127.0.0.1", 5001)
client2 = Client("127.0.0.1", 5002)
client3 = Client("127.0.0.1", 5003)

# Clients send messages
client1.send_message("Hello from Client 1")
client2.send_message("Hello from Client 2")
client3.send_message("Hello from Client 3")

# Print messages stored on each server
server1.print_messages()
server2.print_messages()
server3.print_messages()

# Print hashes stored on each server
server1.print_hashes()
server2.print_hashes()
server3.print_hashes()

# Verify consensus
if server1.verify_consensus():
    print("Consensus achieved: All servers have the same messages.")
else:
    print("Consensus failed: Servers have different message logs.")
