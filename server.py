import pickle
import socket
import threading


from bankaccount import BankAccount
from users import Users
from wallet import Wallet

def handle_client(client_socket, addr):
    try:
        while True:
            request = client_socket.recv(1024)
            command, user_id = pickle.loads(request)
            print("SSSSSSSSSS")
            print(command, user_id)
            if command == "1":  # register
                register_func = Users.register
                # convert to byte
                pickled_function = pickle.dumps(register_func)
                client_socket.send(pickled_function)

            if command == "2": #login
                register_func = Users.login
                # convert to byte
                pickled_function = pickle.dumps(register_func)
                client_socket.send(pickled_function)
            
            if command == "3": #change username
                register_func = Users.change_user_name
                # convert to byte
                pickled_function = pickle.dumps(register_func)
                client_socket.send(pickled_function)
            
            
            
            

            print(f"Received: {request}")
            # convert and send accept response to the client
            response = "accepted"
            client_socket.send(response.encode("utf-8"))
    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


def run_server():
    server_ip = "localhost"
    port = 8000
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, port))
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            thread = threading.Thread(
                target=handle_client,
                args=(
                    client_socket,
                    addr,
                ),
            )
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


run_server()
