import socket
import pickle


# for login | register | logout
def first_menu():
    menu = """
                1. Register
                2. Login
                -1. Logout
            """
    command = None
    while command not in ["1", "2", "-1"]:
        print(menu)
        command = input("Enter command: ")
    return command


def second_menu():
    menu = """
            -1. Logout
            3. change username
            4. change password
            5. rate movie
            6. rate theater
            7. movie comment list
            8. add comment
            9. wallet
            10. bank
            11. add ticket
            """
    command = None
    while command not in ["3", "4", "5", "6", "7", "8", "9", "10", "11", "-1"]:
        print(menu)
        command = input("Enter command: ")
    return command


def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "localhost"
    server_port = 8000
    client.connect((server_ip, server_port))

    try:
        while True:

            def login_register():
                print("in_client: loginRegister")
                command = first_menu()

                # logout
                if command == "-1":
                    return "logout"


                data = pickle.dumps(command)
                
                client.send(data)

                response = client.recv(1024)
                response_func = pickle.loads(response)

                user_id = response_func()
                return user_id

            def application(user_id):
                print("in_client: application start")
                command = second_menu()
                if command == "-1":
                    return "logout"

                data_tuple = (command, user_id)
                data = pickle.dumps(data_tuple)
                client.send(data)
                print("in_client: application data sent")
                

                response = client.recv(1024)
                response_func = pickle.loads(response)
                print("in_client: application recv server response")


                response_func(user_id)

            res1 = login_register()
            if res1 == "logout":
                client.close()
                break
            user_id = res1
            res2 = application(user_id)
            if res2 == "logout":
                client.close()
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection to server closed")


run_client()
