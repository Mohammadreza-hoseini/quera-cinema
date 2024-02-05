# Set root directory
import dotenv, os, sys

dotenv.load_dotenv()
sys.path.insert(0, os.getenv("RootDirectory"))


import hashlib
import re
import uuid

from db_connection.connection import connection
from users import Users
from decorator import admin_login_decorator

cursor = connection.cursor()


class Admin:

    def __init__(self):
        pass

    """ register new admin """

    @staticmethod
    def register(
        username: str, email: str, phone_number: str, password: str, birth_date: str
    ) -> bool:
        if Users.validate_user_name(username) is False:
            return False
        elif Users.validate_email(email) is False:
            return False
        elif Users.validate_phone_number(phone_number) is False:
            return False

        cursor.execute(
            """
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
                              )""",
            (
                "avatar_url",
                username,
                birth_date,
                phone_number,
                email,
                Users.validate_password(password),
                "2024-01-20",
                "2",
                "2024-01-20",
                "admin",
            ),
        )
        connection.commit()
        print("admin registered")
        return True

    """ admin add theater and sit """

    @staticmethod
    @admin_login_decorator
    def add_theater(username: str):
        capacity = input("Enter capacity: ")
        create_uuid = uuid.uuid4()
        cursor.execute(
            f"INSERT INTO Theater (id, capacity, average_rate) VALUES ('{create_uuid}', '{capacity}', -1)"
        )
        connection.commit()
        for item in range(1, int(capacity) + 1):
            cursor.execute(
                f"INSERT INTO Sit (id, theater_id, status) VALUES (uuid(), '{create_uuid}', '0')"
            )
            connection.commit()
        print("insert complete")

    @staticmethod
    def add_movie(name, on_screen_count, age_limit, price):
        if name == "" or name is None:
            print("Enter movie name")
        elif on_screen_count == "" or on_screen_count is None:
            print("Enter screen count")
        elif age_limit == "" or age_limit is None:
            print("Enter age limit")
        elif price == "" or price is None:
            print("Enter price")
        cursor.execute(
            """
            INSERT INTO Movie(id, name, average_rate, on_screen_count,
                              age_limit, price)
                              VALUES (
                              uuid(), %s, %s,
                              %s, %s,
                              %s)""",
            (name, "-1", on_screen_count, age_limit, price),
        )
        connection.commit()
        print("movie registered complete")

    @staticmethod
    def add_schedule(movie_id, theater_id, on_screen_time):
        if movie_id == "" or movie_id is None:
            print("Enter movie_id")
        elif theater_id == "" or theater_id is None:
            print("Enter theater_id")
        elif on_screen_time == "" or on_screen_time is None:
            print("Enter on_screen_time")
        cursor.execute(
            """
            INSERT INTO Schedule(id, movie_id, theater_id, on_screen_time)
                              VALUES (
                              uuid(), %s, %s,
                              %s)""",
            (movie_id, theater_id, on_screen_time),
        )
        connection.commit()
        print("schedule registered complete")


admin_manager = Admin()
# admin_name = input('Enter your username: ')
# email = input('Enter your email: ')
# phone_number = input('Enter your phone number: ')
# birth_date = input("Enter your birth_date with this format 0000-00-00: ")
# password = input("Enter your password")
# admin_manager.register(admin_name, email, phone_number, password, birth_date)
# admin_manager.add_theater()
# admin_manager.add_movie('harry pater', 3, 18, 85000)
admin_manager.add_schedule(
    "a523d397-c33f-11ee-9027-0242ac150202",
    "41ddc2d2-6613-4a53-96ba-97348496d3b7",
    "2024-02-25 15:30:30",
)
