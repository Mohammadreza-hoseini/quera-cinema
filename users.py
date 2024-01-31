import re
import hashlib
from connection import connection

cursor = connection.cursor()


class Users:

    def __init__(self):
        pass

    """validate username"""

    @staticmethod
    def validate_user_name(user_name: str) -> bool:
        if user_name == '' or user_name is None:
            print('enter username')
        # username must be unique,query to db for check it
        cursor.execute(f"SELECT * FROM User1 where username='{user_name}'")
        results = cursor.fetchall()
        if results:
            print('username exist')
        pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{1,100}$')
        result = bool(pattern.match(user_name))
        if result is False:
            return False
        return True

    """validate email"""

    @staticmethod
    def validate_email(user_email: str) -> bool:
        if user_email == '' or user_email is None:
            print('enter email')
        # email must be unique, query to db for check it
        cursor.execute(f"SELECT * FROM User1 where email='{user_email}'")
        results = cursor.fetchall()
        if results:
            print('email exist')
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        result = bool(pattern.match(user_email))
        if result is False:
            return False
        return True

    """validate phone number"""

    @staticmethod
    def validate_phone_number(phone_number: str) -> bool:
        if phone_number == '':
            phone_number = None
            return True
        pattern = re.compile(r'^09\d{9}$')
        result = bool(pattern.match(phone_number))
        if result is False:
            return False
        return True

    """validate password"""

    @staticmethod
    def validate_password(password: str) -> bool:
        if password == '' or password is None:
            print('enter password')
        pattern = r'^(?=.*[a-zA-Z].*[a-zA-Z])(?=.*[@#$&]).{8,}$'
        if not re.match(pattern, password):
            return False
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    """this function for register new user"""

    def register(self, user_name: str, user_email: str, phone_number: str, password: str, birth_date: str):
        if self.validate_user_name(user_name) is False:
            print('username is not valid')
            return False
        elif self.validate_email(user_email) is False:
            print('email is not valid')
            return False
        elif self.validate_phone_number(phone_number) is False:
            print('phone number is not valid')
            return False
        elif self.validate_password(password) is False:
            print('password is not valid')
            return False
        cursor.execute(
            '''
            INSERT INTO User1(uuid, avatar, username, birth_date,
                              phone_number, email, password,
                              register_date, last_login,
                              subscription, bought_subscription_date,
                              role)
                              VALUES (
                              uuid(), %s, %s,
                              %s, %s,
                              %s, %s, current_timestamp, %s,
                              %s, %s, %s
                              )''', ('avatar_url', user_name, birth_date,
                                     phone_number, user_email,
                                     self.validate_password(password), '2024-01-20', '1', '2024-01-20', 'user')
        )
        connection.commit()


user_manager = Users()

username = input("Enter your username: ")
email = input("Enter your email: ")
phone_number = input("Enter your phone number: ")
password = input("Enter your password: ")
birth_date = input("Enter your birth_date with this format 0000-00-00: ")
user_manager.register(username, email, phone_number, password, birth_date)
