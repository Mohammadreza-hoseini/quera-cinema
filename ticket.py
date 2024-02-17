import uuid
from datetime import datetime
from connection import connection
from sit import Sit
import os

cursor = connection.cursor()


class Ticket:
    def __init__(self):
        pass

    @classmethod
    def add_ticket(cls, user_id, schedule_id):

        cursor.execute(
            f"""SELECT theater_name FROM Schedule WHERE id = '{schedule_id}'"""
        )
        theater_name = cursor.fetchone()[0]
        cursor.execute(f"""SELECT id FROM Theater WHERE name = '{theater_name}'""")
        theater_id = cursor.fetchone()[0]

        # select sit section
        empty_theater_sits = Sit.theater_available_sits(theater_id)
        if len(empty_theater_sits) == 0:
            print("No empty sit")
            return
        user_input_sit_id = {}
        row = 0
        print("##### Empty sit ids #####")
        empty_sit_string = ""
        for empty_sit_id in empty_theater_sits:
            row += 1
            empty_sit_string += f"{row}: {empty_sit_id}\n"
        allowed_empty_sit_number = list(range(1, len(empty_theater_sits) + 1))

        print(empty_sit_string)
        selected_sit = input("Enter site id that you selected: ")
        while not selected_sit.isdigit() or int(selected_sit) not in allowed_empty_sit_number:
            print(empty_sit_string)
            selected_sit = input("Enter site id that you selected: ")
        selected_sit = int(selected_sit)
        selected_sit_id = empty_theater_sits[selected_sit - 1]

        # price of movie ticket
        cursor.execute(f"select movie_name from Schedule where id = '{schedule_id}'")
        movie_name_from_schedule = cursor.fetchone()[0]
        cursor.execute(
            f"select Movie.price from Movie where Movie.name = '{movie_name_from_schedule}'"
        )
        price = float(cursor.fetchone()[0])
        # existing sit
        id_generator = str(uuid.uuid4())
        time_generator = str(datetime.now())

        cursor.execute(
            f"insert into Ticket(id, user_id, schedule_id, sit_id, price, bought_time) value ('{id_generator}', '{user_id}', '{schedule_id}', '{selected_sit_id}','{price}', '{time_generator}')"
        )
        Sit.change_status(selected_sit_id)

        connection.commit()
        print("Ticket reserved")
