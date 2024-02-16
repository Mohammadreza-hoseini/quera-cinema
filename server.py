import pickle
import socket
import threading


from bankaccount import BankAccount, bank_menu
from users import Users
from wallet import Wallet, wallet_menu

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

    if command == "2":  # login
        login_func = Users.login
        # convert to byte
        pickled_function = pickle.dumps(login_func)
        client_socket.send(pickled_function)

    if command == "3":  # change username
        change_username_func = Users.change_user_name
        # convert to byte
        pickled_function = pickle.dumps(change_username_func)
        client_socket.send(pickled_function)
    
    if command == "4":  # change password
        change_username_func = Users.change_password
        # convert to byte
        pickled_function = pickle.dumps(change_username_func)
        client_socket.send(pickled_function)
        
        
    if command == "9":  # wallet #TODO
        wallet_menu_func = wallet_menu
        # convert to byte
        pickled_function = pickle.dumps(wallet_menu_func)
        client_socket.send(pickled_function)
    
    if command == "10":  # bank #TODO
        bank_menu_func = bank_menu
        # convert to byte
        pickled_function = pickle.dumps(bank_menu)
        client_socket.send(pickled_function)
    
    print("return request_thread")
    return


def handle_client(client_socket, addr):
    while True:
        try:
            print("waiting for req")
            request = client_socket.recv(1024)
            if not request:
                break
            data = pickle.loads(request)

            print("in_server: handle client", data)

            thread = threading.Thread(
                target=request_thread,
                args=(client_socket, addr, data),
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
    client_socket.close()


def run_server():
    server_ip = "localhost"
    port = 8000
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, port))
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
            print(1)
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            # handle_client(client_socket, addr)
            user_thread = threading.Thread(
                target=handle_client,
                args=(
                    client_socket,
                    addr,
                ),
            )
            user_thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


run_server()

# for thread in thread_list:
#     thread.join()
