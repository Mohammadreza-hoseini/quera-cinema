import uuid
from datetime import datetime
from connection import connection
from sit import Sit

cursor = connection.cursor()


class Ticket:
    def __init__(self):
        pass

    @classmethod
    def add_ticket(cls, user_id, schedule_id):
        # existing user
        cursor.execute(f"select id from User where id = '{user_id}'")
        user_data = cursor.fetchone()
        if user_data is not None:
            user_date = user_data[0]
        else:
            return "User dose not exists"

        # existing schedule
        cursor.execute(f"select id from Schedule where id = '{schedule_id}'")
        schedule_data = cursor.fetchone()
        if schedule_data is not None:
            schedule_data = schedule_data[0]
        else:
            return "Schedule dose not exists"

        # select sit section
        theater_id = input('Enter id of the theater: ')
        empty_theater_sits = Sit.theater_available_sits(theater_id)
        print('Empty sits :', empty_theater_sits)

        selected_sit = input('Enter site id that you selected: ')
        if selected_sit not in empty_theater_sits:
            return f'your selected sit {selected_sit} is not empty list of sits \n <<PLEASE TRY AGAIN>>'
        else:
            # price of movie ticket
            cursor.execute(f"select movie_name from Schedule where id = '{schedule_id}'")
            movie_name_from_schedule = cursor.fetchone()[0]
            cursor.execute(
                f"select Movie.price from Movie where Movie.name = '{movie_name_from_schedule}'")
            price = float(cursor.fetchone()[0])
            # existing sit
            id_generator = str(uuid.uuid4())
            time_generator = str(datetime.now())

            cursor.execute(
                f"insert into Ticket(id, user_id, schedule_id, sit_id, price, bought_time) value ('{id_generator}', '{user_id}', '{schedule_data}', '{selected_sit}','{price}', '{time_generator}')")
            connection.commit()


a = Ticket.add_ticket('99a8fdac-ed21-4d1f-9639-afd6fb68ca7b', '66159c4c-c507-11ee-ad83-0242ac180102')