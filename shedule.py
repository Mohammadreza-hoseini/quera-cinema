from connection import connection

cursor = connection.cursor()


class Schedule:
    def __init__(self):
        pass

    @classmethod
    def add_schedule(cls, movie_id, theater_id, on_screen_time):

        # movie existing query
        cursor.execute(f"SELECT id FROM Movie WHERE id = '{movie_id}'")
        movie_data = cursor.fetchone()

        # movie existing query
        if movie_data is not None:
            movie_data = movie_data[0]
        else:
            return "Movie does not exist "

        # theater existing query
        cursor.execute(f"SELECT id FROM Theater WHERE id = '{theater_id}'")
        theater_data = cursor.fetchone()

        if theater_data is not None:
            theater_id_result = theater_data[0]
        else:
            return "theater does not exist"

        cursor.execute(
            f'insert into Schedule(id, movie_id, theater_id, on_screen_time)values (uuid(),"{movie_data}", "{theater_id_result}", "{on_screen_time}")')
        connection.commit()

    @classmethod
    def time_list(cls):

        cursor.execute(
            f'select * from Schedule where on_screen_time >= now();'
        )
        time_list_date = cursor.fetchall()

        for i in time_list_date:
            cursor.execute(f'select name from Movie where id = "{i[1]}"')
            movie_name = cursor.fetchone()[0]
            cursor.execute(f'select name from Theater where id = "{i[2]}"')
            theater_name = cursor.fetchone()[0]
            print(i[0], movie_name, theater_name, i[3], sep='|---|')


# a = Schedule.add_schedule('10', '41ddc2d2-6613-4a53-96ba-97348496d3b8', '2025-10-11 10:00:00')
Schedule.time_list()
