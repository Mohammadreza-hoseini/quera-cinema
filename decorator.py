# Set root directory
import dotenv, os, sys

dotenv.load_dotenv()
sys.path.insert(0, os.getenv("RootDirectory"))


from db_connection.connection import connection
import hashlib


cursor = connection.cursor()


def user_login_decorator(func):
    def wrapper(*args, **kwargs):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username == "" or username is None:
            print("enter your username")
        elif password == "" or password is None:
            print("enter your password")
        cursor.execute(
            f"SELECT * FROM User where username='{username}' and"
            f" password='{hashlib.sha256(password.encode()).hexdigest()}'"
        )
        results = cursor.fetchall()
        if results:
            cursor.execute(f"UPDATE User SET logged_in='1' where username='{username}'")
            connection.commit()
            print("you are logged in")
        else:
            print("username or password is wrong")
            return False
        func(username)

    return wrapper


def admin_login_decorator(func):
    def wrapper(*args, **kwargs):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username == "" or username is None:
            print("enter your username")
        elif password == "" or password is None:
            print("enter your password")
        cursor.execute(
            f"SELECT * FROM User where username='{username}' and"
            f" password='{hashlib.sha256(password.encode()).hexdigest()}' and role='admin'"
        )
        results = cursor.fetchall()
        if results:
            cursor.execute(f"UPDATE User SET logged_in='1' where username='{username}'")
            connection.commit()
            print("you are logged in")
        else:
            print("username or password is wrong")
            return False
        func(username)

    return wrapper
