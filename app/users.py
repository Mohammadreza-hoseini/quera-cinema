import re
import hashlib
import uuid
from tests.test_db_connection import cnx as connection #connect to test local DB
#from connection import connection
#from rate_to_movies import MovieRate
#from comment import Comment
#from errors import InvalidUsernameOrPassword

# from decorator import user_login_decorator

cursor = connection.cursor()


class Users:

    def __init__(self):
        self.validate_username_dict = {-1: "enter username",-2: "username is invalid",-3: "username exist"}
        self.result = ""
        self.validate_email_dict = {-1: "enter email",-2: "email is invalid",-3: "email exist"}
        self.validate_phone_number_dict = {-1: "phone number is invalid"}
        self.validate_password_dict = {-1: "enter password", -2: "password is invalid"}
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
        user_name = input("Enter your username: ")
        user_validation = self.validate_user_name(user_name)
        if self.validate_username_dict.get(user_validation):
            self.result = self.validate_username_dict[user_validation]
            print(self.result)
            return self.result
        #while user_validation in self.validate_username_dict:
            #self.result = self.validate_username_dict[user_validation]
            #print(self.result)
            #user_name = input("Enter your username: ")
            #user_validation = self.validate_user_name(user_name)
        
        user_email = input("Enter your email: ")
        email_validation = self.validate_email(user_email)
        if self.validate_email_dict.get(email_validation):
            self.result = self.validate_email_dict[email_validation]
            print(self.result)
            return self.result
        #while email_validation in validate_email_dict:
            #print(validate_email_dict[email_validation])
            #user_email = input("Enter your email: ")
            #email_validation = self.validate_email(user_email)
        phone_number = input("Enter your phone number: ")
        if phone_number == "":
            phone_number = None
        phone_number_validation = self.validate_phone_number(phone_number)
        if self.validate_phone_number_dict.get(phone_number_validation):
            self.result = self.validate_phone_number_dict[phone_number_validation]
            print(self.result)
            return self.result
        #while phone_number_validation in validate_phone_number:
            #print(validate_phone_number[phone_number_validation])
            #phone_number = input("Enter your phone number: ")
            #phone_number_validation = self.validate_phone_number(phone_number)
        password = input("Enter your password: ")
        password_validation = self.validate_password(password)
        if self.validate_password_dict.get(password_validation):
            self.result = self.validate_password_dict[password_validation]
            print(self.result)
            return self.result
        #while password_validation in validate_password:
            #print(validate_password[password_validation])
            #password = input("Enter your password: ")
            #password_validation = self.validate_password(password)
        birth_date = input("Enter your birth_date with this format 0000-00-00: ")
        id = uuid.uuid4()

        cursor.execute(f"INSERT INTO User(id, avatar, username, birth_date, phone_number, email, password,"
                       f" register_date, last_login, subscription, bought_subscription_date, role, logged_in)"
                       f" VALUES ('{id}', 'avatar_url', '{user_name}', '{birth_date}', '{phone_number}'"
                       f", '{user_email}', '{password_validation}', current_timestamp, '2024-01-20','2', '2024-01-20',"
                       f" 'user', '1')")
        connection.commit()
        print("registered complete")
        select_action = int(input("For change username enter 1: \nFor change password enter 2: \nFor logout enter 3: "))
        if select_action == 1:
            user_manager.change_user_name(id)
        elif select_action == 2:
            user_manager.change_password(id)
        elif select_action == 3:
            user_manager.logout(id)

    def login(self):
        """this function for user login"""
        user_name = input("Enter your username: ")
        while user_name == "" or user_name is None:
            user_name = input("Enter your username: ")
        password = input("Enter your password: ")
        while password == "" or password is None:
            password = input("Enter your password: ")
        cursor.execute(
            f"SELECT * FROM User where username='{user_name}' and"
            f" password='{self.validate_password(password)}'"
        )
        results = cursor.fetchone()
        try:
            id = results[0]
            cursor.execute(f"UPDATE User SET logged_in='1' where username='{user_name}'")
            connection.commit()
        except InvalidUsernameOrPassword as e:
            print(e)
            return False
        if results:
            print("you are logged in")
            select_action = int(
                input(
                    "For change username enter 1: "
                    "\nFor change password enter 2: "
                    "\nFor logout enter 3: "
                    "\nFor rate to movie enter 4: "
                    "\nFor add comment to movie enter 5: "))
            if select_action == 1:
                user_manager.change_user_name(id)
            elif select_action == 2:
                user_manager.change_password(id)
            elif select_action == 3:
                user_manager.logout(id)
            elif select_action == 4:
                MovieRate.rate_to_movie(id)
            elif select_action == 5:
                Comment.add_comment_to_movie(id)
        else:
            print("username or password is wrong")

    @staticmethod
    # @user_login_decorator
    def change_user_name(id: str) -> None:
        """ this function for change username """
        new_user_name = input("Enter new username: ")
        cursor.execute(
            f"UPDATE User SET username='{new_user_name}' where id='{id}'"
        )
        connection.commit()
        print('username changed')
        select_action = int(input("For change username enter 1: \nFor change password enter 2: \nFor logout enter 3: "))
        if select_action == 1:
            user_manager.change_user_name(id)
        elif select_action == 2:
            user_manager.change_password(id)
        elif select_action == 3:
            user_manager.logout(id)

    # @user_login_decorator
    def change_password(self, id: str) -> None:
        confirm_password_is_vlid = True
        """ this function for change username """
        new_password = input("Enter new password: ")
        validate_password_new_password = {-1: "enter password", -2: "password is invalid"}
        new_password_validation = self.validate_password(new_password)
        while new_password_validation in validate_password_new_password:
            print(validate_password_new_password[new_password_validation])
            new_password = input("Enter new password: ")
            new_password_validation = self.validate_password(new_password)
        confirm_password = input("Enter password again: ")
        validate_confirm_password = {-1: "enter password", -2: "password is invalid"}
        confirm_password_validation = self.validate_password(confirm_password)
        while confirm_password_validation in validate_confirm_password:
            print(validate_confirm_password[confirm_password_validation])
            confirm_password = input("Enter password again: ")
            confirm_password_validation = self.validate_password(confirm_password)
        while new_password != confirm_password:
            confirm_password_is_vlid = False
            print("password not match")
            self.change_password(id)
        cursor.execute(
            f"UPDATE User SET password='{self.validate_password(confirm_password)}' where id='{id}'"
        )
        connection.commit()
        print("password changed")
        select_action = int(input("For change username enter 1: \nFor change password enter 2: \nFor logout enter 3: "))
        if select_action == 1:
            user_manager.change_user_name(id)
        elif select_action == 2:
            user_manager.change_password(id)
        elif select_action == 3:
            user_manager.logout(id)

    @staticmethod
    def logout(id):
        cursor.execute(f"UPDATE User SET logged_in='0' where id='{id}'")
        connection.commit()
        print('log out')


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
