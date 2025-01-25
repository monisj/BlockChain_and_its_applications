    # Send data To the server
    message = "Hello, World!"
    client_socket.send(message.encode('utf-8'))

    # Close the connection
    client_socket.close()