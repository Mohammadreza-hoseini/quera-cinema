import hashlib
import re
import uuid
from datetime import datetime

from connection import connection, redis_client
from users import Users
from errors import MovieNameDoesNotExist, InvalidUsernameOrPassword

# from decorator import admin_login_decorator

cursor = connection.cursor()


class Admin:

    def __init__(self):
        pass

    @staticmethod
    def insert_movies_to_cache() -> None:
        cursor.execute(
            f"""SELECT name, average_rate, age_limit, price FROM Movie ORDER BY average_rate DESC"""
        )
        data = cursor.fetchall()

        movie_list = []
        for movie_tuple in data:
            name, average_rate, age_limit, price = movie_tuple
            movie_data = {
                "name": name,
                "average_rate": average_rate,
                "age_limit": age_limit,
                "price": price,
            }
            movie_list.append(movie_data)
        # redis_client.set('movies', str(movie_list))

    @staticmethod
    def insert_schedules_to_cache(movie_name: str) -> None:
        """
        Returns all available schedules for a movie
        """

        cursor.execute(
            f"""SELECT movie_name, theater_name, on_screen_time FROM Schedule JOIN Theater ON Schedule.theater_name = Theater.name
                               WHERE Schedule.movie_name = {movie_name.__repr__()}
                               ORDER BY Theater.average_rate DESC
                               """
        )
        data = cursor.fetchall()
        available_schedules = []
        for movie_tuple in data:
            movie_name, theater_name, on_screen_time = movie_tuple
            schedule_data = {
                "movie_name": movie_name,
                "theater_name": theater_name,
                "on_screen_time": on_screen_time,
            }
            if on_screen_time >= datetime.now():
                available_schedules.append(schedule_data)
        # redis_client.set('schedules', str(available_schedules))

    @staticmethod
    def register() -> None:
        """ register new admin """
        validate_username_dict = {-1: 'enter username', -2: 'username is invalid', -3: 'username exist'}
        username = input("Enter your username: ")
        user_validation = Users.validate_user_name(username)
        while user_validation in validate_username_dict:
            print(validate_username_dict[user_validation])
            username = input("Enter your username: ")
            user_validation = Users.validate_user_name(username)
        validate_email_dict = {-1: 'enter email', -2: 'email is invalid', -3: 'email exist'}
        user_email = input("Enter your email: ")
        email_validation = Users.validate_email(user_email)
        while email_validation in validate_email_dict:
            print(validate_email_dict[email_validation])
            user_email = input("Enter your email: ")
            email_validation = Users.validate_email(user_email)
        phone_number = input("Enter your phone number: ")
        if phone_number == '':
            phone_number = None
        validate_phone_number = {-1: 'phone number is invalid'}
        phone_number_validation = Users.validate_phone_number(phone_number)
        while phone_number_validation in validate_phone_number:
            print(validate_phone_number[phone_number_validation])
            phone_number = input("Enter your phone number: ")
            phone_number_validation = Users.validate_phone_number(phone_number)
        password = input("Enter your password: ")
        validate_password = {-1: 'enter password', -2: 'password is invalid'}
        password_validation = Users.validate_password(password)
        while password_validation in validate_password:
            print(validate_password[password_validation])
            password = input("Enter your password: ")
            password_validation = Users.validate_password(password)
        birth_date = input("Enter your birth_date with this format 0000-00-00: ")
        id = uuid.uuid4()
        cursor.execute(
            f"INSERT INTO User(id, avatar, username, birth_date, phone_number, email, password, register_date,"
            f" last_login, subscription, bought_subscription_date, role, logged_in) VALUES( '{id}', 'avatar_url',"
            f" '{username}', '{birth_date}', '{phone_number}', '{user_email}', '{Users.validate_password(password)}',"
            f" current_timestamp, '2024-01-20', '2', '2024-01-20', 'admin', '1')")

        connection.commit()
        print('admin registered')
        select_action = int(input(
            "For add theater enter 1: \nFor add movie enter 2: \nFor add schedule enter 3: \nFor logout enter 4: "))
        if select_action == 1:
            admin_manager.add_theater()
        elif select_action == 2:
            admin_manager.add_movie()
        elif select_action == 3:
            admin_manager.add_schedule()
        elif select_action == 4:
            admin_manager.logout(id)

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
            f" password='{Users.validate_password(password)}' and role='admin'"
        )
        results = cursor.fetchone()
        if results is not None:
            id = results[0]
            cursor.execute(f"UPDATE User SET logged_in='1' where username='{user_name}'")
            connection.commit()
        if results:
            print("you are logged in")
            select_action = int(input(
                "For add theater enter 1: \nFor add movie enter 2: \nFor add schedule enter 3: \nFor logout enter 4: "))
            if select_action == 1:
                admin_manager.add_theater()
            elif select_action == 2:
                admin_manager.add_movie()
            elif select_action == 3:
                admin_manager.add_schedule()
            elif select_action == 4:
                admin_manager.logout(id)
        else:
            print("username or password is wrong")

    @staticmethod
    # @admin_login_decorator
    def add_theater() -> None:
        """ admin add theater and sit """
        capacity = input('Enter capacity: ')
        while capacity == '' or capacity is None:
            capacity = input('Enter capacity: ')
        name = input('Enter theater name: ')
        while name == '' or name is None:
            name = input('Enter theater name: ')
        create_uuid = uuid.uuid4()
        cursor.execute(
            f"INSERT INTO Theater (id, capacity, average_rate, name) VALUES ('{create_uuid}', '{capacity}', -1, '{name}')")
        connection.commit()
        for item in range(1, int(capacity) + 1):
            cursor.execute(f"INSERT INTO Sit (id, theater_id, status) VALUES (uuid(), '{create_uuid}', '0')")
            connection.commit()
        print('theater added')
        select_action = int(input(
            "For add theater enter 1: \nFor add movie enter 2: \nFor add schedule enter 3: \nFor logout enter 4: "))
        if select_action == 1:
            admin_manager.add_theater()
        elif select_action == 2:
            admin_manager.add_movie()
        elif select_action == 3:
            admin_manager.add_schedule()
        elif select_action == 4:
            admin_manager.logout(id)

    @staticmethod
    def add_movie():
        """ admin add movie """
        name = input("Enter movie name: ")
        while name == '' or name is None:
            name = input("Enter movie name: ")
        on_screen_count = input("Enter screen count of movie: ")
        while on_screen_count == '' or on_screen_count is None:
            on_screen_count = input("Enter screen count of movie: ")
        age_limit = input("Enter age limit of movie: ")
        while age_limit == '' or age_limit is None:
            age_limit = input("Enter age limit of movie: ")
        price = input("Enter price of movie: ")
        while price == '' or price is None:
            price = input("Enter price of movie: ")
        cursor.execute(
            '''
            INSERT INTO Movie(id, name, average_rate, on_screen_count,
                              age_limit, price)
                              VALUES (
                              uuid(), %s, %s,
                              %s, %s,
                              %s)''', (name, '-1', on_screen_count,
                                       age_limit, price)
        )
        connection.commit()
        # insert data to redis cache
        admin_manager.insert_movies_to_cache()
        print('movie added')
        select_action = int(input(
            "For add theater enter 1: \nFor add movie enter 2: \nFor add schedule enter 3: \nFor logout enter 4: "))
        if select_action == 1:
            admin_manager.add_theater()
        elif select_action == 2:
            admin_manager.add_movie()
        elif select_action == 3:
            admin_manager.add_schedule()
        elif select_action == 4:
            admin_manager.logout(id)

    @staticmethod
    def add_schedule():
        """ admin add schedule """
        movie_name = input("Enter movie_name: ")
        cursor.execute(f"SELECT name FROM Movie WHERE name='{movie_name}'")
        data = cursor.fetchone()
        while movie_name == '' or movie_name is None or not data:
            print('movie name does not exist')
            movie_name = input("Enter movie name: ")
            cursor.execute(f"SELECT name FROM Movie WHERE name='{movie_name}'")
            data = cursor.fetchone()
        theater_name = input("Enter theater name: ")
        cursor.execute(f"SELECT name FROM Theater WHERE name='{theater_name}'")
        data = cursor.fetchone()
        while theater_name == '' or theater_name is None or not data:
            print('theater name does not exist')
            theater_name = input("Enter theater name: ")
            cursor.execute(f"SELECT name FROM Theater WHERE name='{theater_name}'")
            data = cursor.fetchone()
        on_screen_time = input("Enter screen time 0000-00-00 00:00:00 : ")
        while on_screen_time == '' or on_screen_time is None:
            on_screen_time = input("Enter screen time 0000-00-00 00:00:00 : ")
        cursor.execute(
            '''
            INSERT INTO Schedule(id, movie_name, theater_name, on_screen_time)
                              VALUES (
                              uuid(), %s, %s,
                              %s)''', (movie_name, theater_name, on_screen_time)
        )
        connection.commit()
        admin_manager.insert_schedules_to_cache(movie_name)
        print('schedule added')
        select_action = int(input(
            "For add theater enter 1: \nFor add movie enter 2: \nFor add schedule enter 3: \nFor logout enter 4: "))
        if select_action == 1:
            admin_manager.add_theater()
        elif select_action == 2:
            admin_manager.add_movie()
        elif select_action == 3:
            admin_manager.add_schedule()
        elif select_action == 4:
            admin_manager.logout(id)

    @staticmethod
    def logout(id):
        cursor.execute(f"UPDATE User SET logged_in='0' where id='{id}'")
        connection.commit()
        print('log out')


admin_manager = Admin()

while True:
    chose_login_or_register = int(input("For register enter 1: \nFor login enter 2: "))
    if chose_login_or_register == 1:
        admin_manager.register()
    elif chose_login_or_register == 2:
        admin_manager.login()
