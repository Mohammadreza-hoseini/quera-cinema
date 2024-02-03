from connection import connection
import hashlib

cursor = connection.cursor()

# close connection at the end #TODO:


def BA_login_decorator(func):
    def wrapper(*args, **kwargs):  # no need for
        print("Bank_account login: \n")
        username = input("Enter your username: ")
        password = input("Enter your bank_account password: ")

        cursor.execute(f"SELECT id FROM User where username = {username.__repr__()}")
        user_id = cursor.fetchone()[0]
        if user_id is not None:

            cursor.execute(
                f"SELECT password FROM BankAccount where user_id = {user_id.__repr__()}"
            )
            user_bankAccounts_password_list = (
                cursor.fetchall()
            )  # returns list of tuples
            if user_bankAccounts_password_list is not None:
                print("DDDDDDDDDDDDDDDDDD", password)
                print(user_bankAccounts_password_list)
                entered_hashed_pass = hashlib.sha256(password.encode()).hexdigest()
                for hash_pass_tuples in user_bankAccounts_password_list:
                    if entered_hashed_pass in hash_pass_tuples:
                        print("logged in")
                        break
                else:
                    print("Invalid credentials")
                    return False
            else:
                print("User doesn't have an account")
                return False
        else:
            print("User doesn't exist")
            return False
        func(*args, **kwargs)

    return wrapper


def user_login_decorator(func):
    def wrapper(*args, **kwargs):
        print("App login: \n")
        username = input("Enter your username: ")
        password = input("Enter your App password: ")
        if username == "" or username is None:
            print("enter your username")
        elif password == "" or password is None:
            print("enter your password")
        cursor.execute(
            f"SELECT * FROM User where username={username.__repr__()} and"
            f" password='{hashlib.sha256(password.encode()).hexdigest()}'"
        )
        results = cursor.fetchall()
        if results is not None:
            print("you are logged in")
        else:
            print("username or password is wrong")
            return False
        func(*args, **kwargs)

    return wrapper
