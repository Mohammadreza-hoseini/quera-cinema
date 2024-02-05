# Set root directory
import dotenv, os, sys

dotenv.load_dotenv()
sys.path.insert(0, os.getenv("RootDirectory"))

import re
import hashlib
from db_connection.connection import connection

# from decorator import user_login_decorator

cursor = connection.cursor()


class Users:

    def __init__(self):
        pass

    @staticmethod
    def validate_user_name(user_name: str) -> bool:
        """validate username"""
        if user_name == "" or user_name is None:
            return -1
        # username must be unique,query to db for check it
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{1,100}$")
        result = bool(pattern.match(user_name))
        if result is False:
            return -2

        cursor.execute(f"SELECT * FROM User where username='{user_name}'")
        results = cursor.fetchall()
        if results:
            return -3
        return True

    @staticmethod
    def validate_email(user_email: str) -> bool:
        """validate email"""
        if user_email == "" or user_email is None:
            return -1
        pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        result = bool(pattern.match(user_email))
        if result is False:
            return -2
        # email must be unique, query to db for check it
        cursor.execute(f"SELECT * FROM User where email='{user_email}'")
        results = cursor.fetchall()
        if results:
            return -3
        return True

    @staticmethod
    def validate_phone_number(phone_number: str) -> bool:
        """validate phone number"""
        if phone_number is None:
            return True
        pattern = re.compile(r'^09\d{9}$')
        result = bool(pattern.match(phone_number))
        if result is False:
            return -1
        return True

    @staticmethod
    def validate_password(password: str) -> bool:
        """validate password"""
        if password == "" or password is None:
            return -1
        pattern = r"^(?=.*[a-zA-Z].*[a-zA-Z])(?=.*[@#$&]).{8,}$"
        if not re.match(pattern, password):
            return -2
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def register(self):
        """this function for register new user"""
        validate_username_dict = {
            -1: "enter username",
            -2: "username is invalid",
            -3: "username exist",
        }
        user_name = input("Enter your username: ")
        user_validation = self.validate_user_name(user_name)
        while user_validation in validate_username_dict:
            user_name = input("Enter your username: ")
            user_validation = self.validate_user_name(user_name)
        validate_email_dict = {
            -1: "enter email",
            -2: "email is invalid",
            -3: "email exist",
        }
        user_email = input("Enter your email: ")
        email_validation = self.validate_email(user_email)
        while email_validation in validate_email_dict:
            user_email = input("Enter your email: ")
            email_validation = self.validate_email(user_email)
        phone_number = input("Enter your phone number: ")
        if phone_number == "":
            phone_number = None
        validate_phone_number = {-1: "phone number is invalid"}
        phone_number_validation = self.validate_phone_number(phone_number)
        while phone_number_validation in validate_phone_number:
            phone_number = input("Enter your phone number: ")
            phone_number_validation = self.validate_phone_number(phone_number)
        password = input("Enter your password: ")
        validate_password = {-1: "enter password", -2: "password is invalid"}
        password_validation = self.validate_password(password)
        while password_validation in validate_password:
            password = input("Enter your password: ")
            password_validation = self.validate_password(password)
        birth_date = input("Enter your birth_date with this format 0000-00-00: ")
        cursor.execute(
            """
            INSERT INTO User(id, avatar, username, birth_date,
                              phone_number, email, password,
                              register_date, last_login,
                              subscription, bought_subscription_date,
                              role, logged_in)
                              VALUES (
                              uuid(), %s, %s,
                              %s, %s,
                              %s, %s, current_timestamp, %s,
                              %s, %s, %s, %s
                              )""",
            (
                "avatar_url",
                user_name,
                birth_date,
                phone_number,
                user_email,
                self.validate_password(password),
                "2024-01-20",
                "2",
                "2024-01-20",
                "user",
                "1",
            ),
        )
        connection.commit()
        print("registered complete")

    @staticmethod
    def login():
        """this function for user login"""
        user_name = input("Enter your username: ")
        while user_name == "" or user_name is None:
            user_name = input("Enter your username: ")
        password = input("Enter your password: ")
        while password == "" or password is None:
            password = input("Enter your password: ")
        cursor.execute(
            f"SELECT * FROM User where username='{user_name}' and"
            f" password='{hashlib.sha256(password.encode()).hexdigest()}'"
        )
        results = cursor.fetchall()
        cursor.execute(f"UPDATE User SET logged_in='1' where username='{user_name}'")
        connection.commit()
        if results:
            print("you are logged in")
        else:
            print("username or password is wrong")

    @staticmethod
    # @user_login_decorator
    def change_user_name(user_name) -> bool:
        """ this function for change username """
        new_user_name = input("Enter new username: ")
        cursor.execute(
            f"UPDATE User SET username='{new_user_name}' where username='{user_name}'"
        )
        connection.commit()

    @staticmethod
    # @user_login_decorator
    def change_password(user_name: str) -> bool:
        """ this function for change username """
        new_password = input("Enter new password: ")
        confirm_password = input("Enter password again: ")
        if new_password != confirm_password:
            print("password is not match")
            return False
        cursor.execute(
            f"UPDATE User SET password='{hashlib.sha256(new_password.encode()).hexdigest()}' where username='{user_name}'"
        )
        connection.commit()
        print("password change")


user_manager = Users()


def main():
    while True:
        chose_login_or_register = int(
            input(
                "For register enter 1: \nFor login enter 2: "))
        if chose_login_or_register == 1:
            user_manager.register()
        elif chose_login_or_register == 2:
            user_manager.login()


if __name__ == "__main__":
    main()