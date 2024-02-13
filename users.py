import re
import hashlib
import uuid
from datetime import datetime

from connection import connection
from rate_to_movies import MovieRate
from comment import Comment
from errors import InvalidUsernameOrPassword, InvalidDate
from wallet import Wallet
from help_function import is_float

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

    @staticmethod
    def register():
        """this function for register new user"""
        validate_username_dict = {
            -1: "enter username",
            -2: "username is invalid",
            -3: "username exist",
        }
        user_name = input("Enter your username: ")
        user_validation = Users.validate_user_name(user_name)
        while user_validation in validate_username_dict:
            print(validate_username_dict[user_validation])
            user_name = input("Enter your username: ")
            user_validation = Users.validate_user_name(user_name)
        validate_email_dict = {
            -1: "enter email",
            -2: "email is invalid",
            -3: "email exist",
        }
        user_email = input("Enter your email: ")
        email_validation = Users.validate_email(user_email)
        while email_validation in validate_email_dict:
            print(validate_email_dict[email_validation])
            user_email = input("Enter your email: ")
            email_validation = Users.validate_email(user_email)
        phone_number = input("Enter your phone number: ")
        if phone_number == "":
            phone_number = None
        validate_phone_number = {-1: "phone number is invalid"}
        phone_number_validation = Users.validate_phone_number(phone_number)
        while phone_number_validation in validate_phone_number:
            print(validate_phone_number[phone_number_validation])
            phone_number = input("Enter your phone number: ")
            phone_number_validation = Users.validate_phone_number(phone_number)
        password = input("Enter your password: ")
        validate_password = {-1: "enter password", -2: "password is invalid"}
        password_validation = Users.validate_password(password)
        while password_validation in validate_password:
            print(validate_password[password_validation])
            password = input("Enter your password: ")
            password_validation = Users.validate_password(password)
        birth_date = input("Enter your birth_date with this format 0000-00-00: ")
        pattern_str = r'^\d{4}-\d{2}-\d{2}$'
        while not re.match(pattern_str, birth_date):
            birth_date = input("Enter your birth_date with this format 0000-00-00: ")
            print(birth_date)
        id = uuid.uuid4()

        cursor.execute(f"INSERT INTO User(id, avatar, username, birth_date, phone_number, email, password,"
                       f" register_date, last_login, subscription, bought_subscription_date, role, logged_in)"
                       f" VALUES ('{id}', 'avatar_url', '{user_name}', '{birth_date}', '{phone_number}'"
                       f", '{user_email}', '{password_validation}', current_timestamp, '2024-01-20','2', '2024-01-20',"
                       f" 'user', '1')")
        connection.commit()
        print("registered complete")
        Wallet.create_wallet(id)
        return id
        # select_action = input("For change username enter 1: \nFor change password enter 2: \nFor logout enter -1: ")
        # while select_action not in ['1', '2', '-1']:
        #     select_action = input(
        #         "For change username enter 1: \nFor change password enter 2: \nFor logout enter -1: "
        #         "\nFor rate to movie enter 4: \nFor add comment to movie enter 5: ")
        # if select_action == '1':
        #     user_manager.change_user_name(id)
        # elif select_action == '2':
        #     user_manager.change_password(id)
        # elif select_action == '-1':
        #     user_manager.logout(id)
        # elif select_action == '4':
        #     MovieRate.rate_to_movie(id)
        # elif select_action == '5':
        #     Comment.add_comment_to_movie(id)

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
            f" password='{Users.validate_password(password)}'"
        )
        results = cursor.fetchone()
        while results is None:
            print('Username or Password is wrong')
            user_name = input("Enter your username: ")
            while user_name == "" or user_name is None:
                user_name = input("Enter your username: ")
            password = input("Enter your password: ")
            while password == "" or password is None:
                password = input("Enter your password: ")
            cursor.execute(
                f"SELECT * FROM User where username='{user_name}' and"
                f" password='{Users.validate_password(password)}'"
            )
            results = cursor.fetchone()
        id = results[0]
        cursor.execute(f"UPDATE User SET logged_in='1' where username='{user_name}'")
        connection.commit()
        print("you are logged in")
        return id
        # select_action = input(
        #     "For change username enter 1: "
        #     "\nFor change password enter 2: "
        #     "\nFor logout enter -1: "
        #     "\nFor rate to movie enter 4: "
        #     "\nFor add comment to movie enter 5: "
        #     "\nFor Wallet enter 6: ")
        # while select_action not in ['1', '2', '-1', '4', '5', '6']:
        #     select_action = input(
        #         "For change username enter 1: "
        #         "\nFor change password enter 2: "
        #         "\nFor logout enter -1: "
        #         "\nFor rate to movie enter 4: "
        #         "\nFor add comment to movie enter 5: "
        #         "\nFor Wallet enter 6: ")
        # if select_action == '1':
        #     user_manager.change_user_name(id)
        # elif select_action == '2':
        #     user_manager.change_password(id)
        # elif select_action == '-1':
        #     user_manager.logout(id)
        # elif select_action == '4':
        #     MovieRate.rate_to_movie(id)
        # elif select_action == '5':
        #     Comment.add_comment_to_movie(id)
        # elif select_action == '6':
        #     select_action = input(
        #             'For wallet balance enter 1: \nFor pay from wallet enter 2: ')
        #     while select_action not in ['1', '2']:
        #         select_action = input(
        #             'For wallet balance enter 1: \nFor pay from wallet enter 2: ')
        #     if select_action == '1':
        #         Wallet.wallet_balance(id)
        #     elif select_action == '2':
        #         transaction_amount = input('Enter amount of transaction')
        #         while not is_float(transaction_amount):
        #             transaction_amount = input('Enter amount of transaction')
        #         Wallet.pay_from_wallet(id, float(transaction_amount))

    # @user_login_decorator
    @staticmethod
    def change_user_name(id: str) -> None:
        """ this function for change username """
        validate_username_dict = {
            -1: "enter username",
            -2: "username is invalid",
            -3: "username exist",
        }
        new_user_name = input("Enter new username: ")
        user_validation = Users.validate_user_name(new_user_name)
        while user_validation in validate_username_dict:
            print(validate_username_dict[user_validation])
            new_user_name = input("Enter new username: ")
            user_validation = Users.validate_user_name(new_user_name)
        cursor.execute(
            f"UPDATE User SET username='{new_user_name}' where id='{id}'"
        )
        connection.commit()
        print('username changed')
        # select_action = input("For change username enter 1: \nFor change password enter 2: \nFor logout enter -1: ")
        # while select_action not in ['1', '2', '-1']:
        #     select_action = input(
        #         "For change username enter 1: \nFor change password enter 2: \nFor logout enter -1: "
        #         "\nFor rate to movie enter 4: \nFor add comment to movie enter 5: ")
        # if select_action == '1':
        #     user_manager.change_user_name(id)
        # elif select_action == '2':
        #     user_manager.change_password(id)
        # elif select_action == '-1':
        #     user_manager.logout(id)
        # elif select_action == '4':
        #     MovieRate.rate_to_movie(id)
        # elif select_action == '5':
        #     Comment.add_comment_to_movie(id)

    # @user_login_decorator
    @staticmethod
    def change_password(id: str) -> None:
        """ this function for change username """
        new_password = input("Enter new password: ")
        validate_password_new_password = {-1: "enter password", -2: "password is invalid"}
        new_password_validation = Users.validate_password(new_password)
        while new_password_validation in validate_password_new_password:
            print(validate_password_new_password[new_password_validation])
            new_password = input("Enter new password: ")
            new_password_validation = Users.validate_password(new_password)
        confirm_password = input("Enter password again: ")
        validate_confirm_password = {-1: "enter password", -2: "password is invalid"}
        confirm_password_validation = Users.validate_password(confirm_password)
        while confirm_password_validation in validate_confirm_password:
            print(validate_confirm_password[confirm_password_validation])
            confirm_password = input("Enter password again: ")
            confirm_password_validation = Users.validate_password(confirm_password)
        while new_password != confirm_password:
            print("password not match")
            Users.change_password(id)
        cursor.execute(
            f"UPDATE User SET password='{Users.validate_password(confirm_password)}' where id='{id}'"
        )
        connection.commit()
        print("password changed")
        # select_action = input("For change username enter 1: \nFor change password enter 2: \nFor logout enter -1: ")
        # while select_action not in ['1', '2', '-1']:
        #     select_action = input(
        #         "For change username enter 1: \nFor change password enter 2: \nFor logout enter -1: "
        #         "\nFor rate to movie enter 4: \nFor add comment to movie enter 5: ")
        # if select_action == '1':
        #     user_manager.change_user_name(id)
        # elif select_action == '2':
        #     user_manager.change_password(id)
        # elif select_action == '-1':
        #     user_manager.logout(id)
        # elif select_action == '4':
        #     MovieRate.rate_to_movie(id)
        # elif select_action == '5':
        #     Comment.add_comment_to_movie(id)

    @staticmethod
    def logout(id):
        cursor.execute(f"UPDATE User SET logged_in='0' where id='{id}'")
        connection.commit()
        print('log out')


user_manager = Users()


def main():
    chose_login_or_register = int(
        input(
            "For register enter 1: \nFor login enter 2: "))
    if chose_login_or_register == 1:
        user_manager.register()
    elif chose_login_or_register == 2:
        user_manager.login()


if __name__ == "__main__":
    main()
