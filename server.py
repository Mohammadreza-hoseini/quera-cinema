import socket


# Define host and port
HOST = '127.0.0.1'
PORT = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)

print(f"Server is listening on {HOST}:{PORT}")

# Accept incoming connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

while True:
    # Receive data from the client
    data = conn.recv(1024)
    if not data:
        break
    print(f"Received: {data.decode('utf-8')}")
    data_decode = data.decode('utf-8')
    # Send a response back to the client
    conn.sendall(b"Message received!")
    # conn.sendall(x.encode())

# Close the connection
conn.close()
