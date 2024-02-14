import pickle
import socket
import threading


from bankaccount import BankAccount
from users import Users
from wallet import Wallet

# thread_list = []

def request_thread(client_socket, addr, data):
    print("in_server: request_thread")
    
    if isinstance(data, tuple):
        command, user_id = data
    else:
        command = data

                
    if command == "1":  # register
        register_func = Users.register
        # convert to byte
        pickled_function = pickle.dumps(register_func)
        client_socket.send(pickled_function)

    if command == "2": #login
        login_func = Users.login
        # convert to byte
        pickled_function = pickle.dumps(login_func)
        client_socket.send(pickled_function)
    
    if command == "3": #change username
        change_username_func = Users.change_user_name
        # convert to byte
        pickled_function = pickle.dumps(change_username_func)
        print("hereee")
        client_socket.send(pickled_function)
        print("in_server: function sent")
    print("return request_thread")
    return
        
def handle_client(client_socket, addr):
    while True:
        try:
            request = client_socket.recv(1024)
            data = pickle.loads(request)
            
            print("in_server: handle client", data)
            
            
            
            thread = threading.Thread(
                target=request_thread,
                args=(
                    client_socket,
                    addr, data
                ),
            )
            # thread_list.append(thread)
            print("thread start")
            thread.start()
            print("thread waiting")
            thread.join()
            print("thread finished")
            
        except Exception as e:
            print(f"Error when hanlding client: {e}")
            break
        # finally:
        #     # thread.join()
        #     print("thread finished")
            
        #     client_socket.close()
        #     print(f"Connection to client ({addr[0]}:{addr[1]}) closed")
        #     break


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
            handle_client(client_socket, addr)
            # thread = threading.Thread(
            #     target=handle_client,
            #     args=(
            #         client_socket,
            #         addr,
            #     ),
            # )
            # thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


run_server()

# for thread in thread_list:
#     thread.join()