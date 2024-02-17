from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import uuid

from connection import connection, redis_client
from schedule import Schedule
from ticket import Ticket

cursor = connection.cursor()


class Movie:
    def __init__(self, name, age_limit):
        self.uuid = uuid.uuid4()
        self.name = name
        self.age_limit = age_limit

    @staticmethod
    def movie_list(user_id):
        cursor.execute(f"""SELECT birth_date FROM User WHERE id = '{user_id}'""")
        user_birth_date = cursor.fetchone()[0]
        user_birth_date = user_birth_date.date()
        today = date.today()
        user_age = today - user_birth_date
        user_age = relativedelta(today, user_birth_date).years
        if 1 == 2:  # never runs
            get_data_from_cache = redis_client.get("movies")
            if get_data_from_cache is not None:
                return get_data_from_cache
        else:
            cursor.execute(
                f"""SELECT name, average_rate, age_limit, price FROM Movie WHERE age_limit <= {user_age} ORDER BY average_rate DESC"""
            )
            data = cursor.fetchall()
            if len(data) == 0:
                print("No movie for your age")
                return

            movie_list = []
            row = 0
            print("name, average_rate, age_limit, price")
            for movie_tuple in data:
                name, average_rate, age_limit, price = movie_tuple
                row += 1
                print(f"{row}: {name}, {average_rate}, {age_limit}, {price}")
                movie_data = {
                    "name": name,
                    "average_rate": average_rate,
                    "age_limit": age_limit,
                    "price": price,
                }
                movie_list.append(movie_data)
            # return movie_list

    @staticmethod
    def average_rate() -> str:
        try:
            cursor.execute(f'SELECT average_rate FROM Movie WHERE name="{name}"')
            return cursor.fetchone()[0]
        except Exception as e:
            return "Movie doesn't exist"

    @staticmethod
    def on_screen_count() -> str:
        cursor.execute(f'SELECT COUNT(*) FROM Schedule WHERE movie_id = "%{uuid}"')
        return cursor.fetchone()[0]

    @staticmethod
    def choose_movie(user_id: str) -> None:
        movie_name = input("Enter movie name: ")
        cursor.execute(f"""SELECT 1 FROM Movie WHERE name='{movie_name}'""")
        data = cursor.fetchone()
        while data is None:
            movie_name = input("Enter movie name: ")
            cursor.execute(f"""SELECT 1 FROM Movie WHERE name='{movie_name}'""")
            data = cursor.fetchone()

        available_schedules = Schedule.all_available_schedules(movie_name)
        if available_schedules == -1:
            return
        schedule_allowed_numbers = len(available_schedules)
        selected_schedule = input("Enter number of schedule: ")
        allowed_numbers = list(range(1, schedule_allowed_numbers + 1))
        while not selected_schedule.isdigit() or int(selected_schedule) not in allowed_numbers:
            selected_schedule = input("Enter number of schedule: ")
        selected_schedule = int(selected_schedule)

        selected_schedule_id = available_schedules[selected_schedule - 1]["id"]

        Ticket.add_ticket(user_id, selected_schedule_id)

    def __str__(self):
        return self.name
