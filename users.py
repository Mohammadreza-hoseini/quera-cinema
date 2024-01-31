import re


class Users:

    def __init__(self):
        pass

    """validate username"""

    @staticmethod
    def validate_user_name(user_name: str) -> bool:
        # username must be unique,query to db for check it
        pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{1,100}$')
        result = bool(pattern.match(user_name))
        if result is False:
            return False
        return True

    """validate email"""

    @staticmethod
    def validate_email(user_email: str) -> bool:
        # email must be unique, query to db for check it
        pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        result = bool(pattern.match(user_email))
        if result is False:
            return False
        return True

    """validate phone number"""

    @staticmethod
    def validate_phone_number(phone_number: str) -> bool:
        pattern = re.compile(r'^09\d{9}$')
        result = bool(pattern.match(phone_number))
        if result is False:
            return False
        return True

    """this function for register new user"""

    def register(self, user_name: str, user_email: str, phone_number: str):
        if self.validate_user_name(user_name) is False:
            print('username is not valid')
        elif self.validate_email(user_email) is False:
            print('email is not valid')
        elif self.validate_phone_number(phone_number) is False:
            print('phone number is not valid')


user_manager = Users()

username = input("Enter your username: ")
email = input("Enter your email: ")
phone_number = input("Enter your phone number: ")
user_manager.register(username, email, phone_number)
