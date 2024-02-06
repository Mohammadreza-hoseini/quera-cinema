from connection import connection
from datetime import datetime


cursor = connection.cursor()


class Schedule:
    def __init__(self):
        pass

    @staticmethod
    def all_available_schedules(movie_name: str):
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
        available_movies = []
        for movie_tuple in data:
            movie_name, theater_name, on_screen_time = movie_tuple
            schedule_data = {
                "movie_name": movie_name,
                "theater_name": theater_name,
                "on_screen_time": on_screen_time,
            }
            if on_screen_time >= datetime.now():
                available_movies.append(schedule_data)
        print(available_movies)


if __name__ == "__main__":
    # a = Schedule.add_schedule('10', '41ddc2d2-6613-4a53-96ba-97348496d3b8', '2025-10-11 10:00:00')
    Schedule.all_available_schedules("hasanii")
