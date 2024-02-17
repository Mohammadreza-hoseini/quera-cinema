import socket
import pickle


from bankaccount import BankAccount
from help_function import is_float

bank_login = BankAccount.login


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
            7. movie list
            8. add comment
            9. wallet
            10. bank
            11. add ticket
            12. choose movie
            """
    command = None
    while command not in ["3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "-1"]:
        print(menu)
        command = input("Enter command: ")
    return command


def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "localhost"
    server_port = 8000
    # print("run_client")
    client.connect((server_ip, server_port))

    try:
        login_status = 0
        bank_login_status = 0
        while True:

            def login_register():
                # print("in_client: loginRegister")
                command = first_menu()

                # logout
                if command == "-1":
                    return "logout"

                data = pickle.dumps(command)

                client.send(data)

                response = client.recv(1024)
                response_func = pickle.loads(response)

                # print("NAAAAAAAAAAAAAAAme")
                # print(response_func.__name__)

                user_id = response_func()
                return user_id

            def application(user_id):
                nonlocal bank_login_status
                # print("in_client: application start")
                command = second_menu()
                if command == "-1":
                    return "logout"

                # bank
                if command == "10" and bank_login_status == 0:  # not logged in bank
                    data = bank_login(user_id)
                    if data == -2:  # user doesn't have bank account
                        return
                    else:
                        card_number = data
                        bank_login_status = 1

                data_tuple = (command, user_id)
                data = pickle.dumps(data_tuple)
                client.send(data)
                # print("in_client: application data sent")

                response = client.recv(1024)
                response_func = pickle.loads(response)
                # print("in_client: application recv server response")

                # give function inputs based on its name
                func_name = response_func.__name__

                if func_name in [
                    "change_password",
                    "change_user_name",
                    "rate_to_movie",
                    "rate_theater",
                    "movie_list",
                    "choose_movie",
                ]:

                    response_func(user_id)

                # handle wallet
                if func_name == "wallet_menu":
                    wallet_operation = response_func()
                    if wallet_operation == -1:
                        return "logout"
                    if wallet_operation.__name__ == "pay_from_wallet":
                        transaction_amount = None
                        while transaction_amount is None or not is_float(
                            transaction_amount
                        ):
                            print("Transaction_amount should be float")
                            transaction_amount = input("Enter transaction amount: ")
                        wallet_operation(user_id, float(transaction_amount))
                    if wallet_operation.__name__ == "wallet_balance":
                        current_wallet_balance = wallet_operation(user_id)
                        print("current wallet balance: ", current_wallet_balance)

                # handle bank_account
                if func_name == "bank_menu":
                    bank_operation = response_func()

                    if bank_operation == -1:
                        bank_login_status = 0
                        print("Logged out of bank account")
                        return

                    transaction_amount = None
                    while transaction_amount is None or not is_float(
                        transaction_amount
                    ):
                        print("Transaction_amount should be float")
                        transaction_amount = input("Enter transaction amount: ")
                    transaction_amount = float(transaction_amount)

                    if bank_operation.__name__ == "charge_wallet":
                        bank_operation(user_id, card_number, transaction_amount)
                    else:
                        bank_operation(card_number, transaction_amount)

            if login_status == 0:
                res1 = login_register()
                if res1 == "logout":
                    break
                else:
                    login_status = 1
                user_id = res1
            res2 = application(user_id)
            if res2 == "logout":
                break
        client.close()

    except Exception as e:
        # print("after breakkkk")
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection to server closed")


run_client()
