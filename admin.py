import re
import hashlib
from connection import connection
from users import Users
from decorator import admin_login_decorator
import uuid

cursor = connection.cursor()


class Admin:

    def __init__(self):
        pass

    """ register new admin """

    @staticmethod
    def register(username: str, email: str, phone_number: str, password: str, birth_date: str) -> bool:
        if Users.validate_user_name(username) is False:
            return False
        elif Users.validate_email(email) is False:
            return False
        elif Users.validate_phone_number(phone_number) is False:
            return False

        cursor.execute(
            '''
            INSERT INTO User(id, avatar, username, birth_date,
                              phone_number, email, password,
                              register_date, last_login,
                              subscription, bought_subscription_date,
                              role)
                              VALUES (
                              uuid(), %s, %s,
                              %s, %s,
                              %s, %s, current_timestamp, %s,
                              %s, %s, %s
                              )''', ('avatar_url', username, birth_date,
                                     phone_number, email,
                                     Users.validate_password(password), '2024-01-20', '2', '2024-01-20', 'admin')
        )
        connection.commit()
        print('admin registered')
        return True

    """ admin add theater and sit """
    @staticmethod
    @admin_login_decorator
    def add_theater(username: str):
        capacity = input('Enter capacity: ')
        create_uuid = uuid.uuid4()
        cursor.execute(f"INSERT INTO Theater (id, capacity, average_rate) VALUES ('{create_uuid}', '{capacity}', -1)")
        connection.commit()
        for item in range(1, int(capacity)+1):
            cursor.execute(f"INSERT INTO Sit (id, theater_id, status) VALUES (uuid(), '{create_uuid}', '0')")
            connection.commit()
        print('insert complete')


admin_manager = Admin()
# admin_name = input('Enter your username: ')
# email = input('Enter your email: ')
# phone_number = input('Enter your phone number: ')
# birth_date = input("Enter your birth_date with this format 0000-00-00: ")
# password = input("Enter your password")
# admin_manager.register(admin_name, email, phone_number, password, birth_date)
admin_manager.add_theater()
for item in range(1, 30+1):
    ...
