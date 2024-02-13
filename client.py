import socket
from users import chose_input

# Define host and port
HOST = '127.0.0.1'
PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Send data to the server
client_socket.sendall(b"1")

# Receive response from the server
response = client_socket.recv(1024)

choose_your_input = chose_input(1)
print(choose_your_input)

print(f"Response from server: {response.decode('utf-8')}")

# Close the connection
client_socket.close()
