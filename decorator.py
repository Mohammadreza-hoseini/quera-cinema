from connection import connection
import hashlib

cursor = connection.cursor()


def login_decorator(func):
    def wrapper(*args, **kwargs):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username == '' or username is None:
            print('enter your username')
        elif password == '' or password is None:
            print('enter your password')
        cursor.execute(
            f"SELECT * FROM User where username='{username}' and"
            f" password='{hashlib.sha256(password.encode()).hexdigest()}'")
        results = cursor.fetchall()
        if results:
            print('you are logged in')
        else:
            print('username or password is wrong')
            return False
        func(username)

    return wrapper
