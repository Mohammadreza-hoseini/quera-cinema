from connection import connection

cursor = connection.cursor()


class Schedule:
    def __init__(self):
        pass

    @classmethod
    def Add_Schedule(cls, movie_id, theater_id, on_screen_time):

        # movie existing query
        cursor.execute(f"SELECT id FROM Movie WHERE id = {movie_id}")
        movie_data = cursor.fetchone()

        if movie_data is not None:
            movie_id_result = movie_data[0]
        else:
            return "Movie does not exist"

        # theater existing query
        cursor.execute(f"SELECT id FROM Theater WHERE id = {theater_id}")
        theater_data = cursor.fetchone()

        if theater_data is not None:
            theater_id_result = theater_data[0]
        else:
            return "Movie does not exist"

        cursor.execute(
            f'insert into Schedule(id, movie_id, theater_id, on_screen_time)values (uuid(),\
             {movie_id_result.__repr__()}, {theater_id_result.__repr__()}, {on_screen_time.__repr__()})')
        connection.commit()


a = Schedule.Add_Schedule('10', '1', '2023-10-10 11:00:00')
