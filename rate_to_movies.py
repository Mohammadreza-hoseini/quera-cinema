import re
import hashlib
import uuid

from connection import connection
from errors import MovieNameDoesNotExist, InvalidArguments


cursor = connection.cursor()


class MovieRate:
    def __init__(self):
        pass

    @staticmethod
    def rate_to_movie(user_id):
        """this function for add rate to movie"""

        rate = input("Enter your rate: ")
        valid_rates = ["1", "2", "3", "4", "5"]
        while rate not in valid_rates:
            print("Rate should be from 1 to 5")
            rate = input("Enter your rate: ")
        movie_name = input("Enter name of movie: ")
        while movie_name == "" or movie_name is None:
            movie_name = input("Enter name of movie: ")
        cursor.execute(f"SELECT id FROM Movie WHERE name='{movie_name}'")
        result = cursor.fetchone()
        while result is None:
            print("Movie doesn't exist")
            movie_name = input("Enter name of movie: ")
            while movie_name == "" or movie_name is None:
                movie_name = input("Enter name of movie: ")
            cursor.execute(f"SELECT id FROM Movie WHERE name='{movie_name}'")
            result = cursor.fetchone()
        movie_id = result[0]

        # check if user rated this movie before #TODO
        cursor.execute(
            f"SELECT 1 FROM MovieRateTable WHERE movie_id='{movie_id}' AND user_id='{user_id}'"
        )
        if cursor.fetchone():  # user rate movie exists
            print("You have already rated this movie")
            return

        cursor.execute(
            f"INSERT INTO MovieRateTable(rate, movie_id, user_id)"
            f"VALUES ('{rate}', '{movie_id}', '{user_id}')"
        )

        # update movie average rate:
        cursor.execute(f"""SELECT AVG(rate) FROM MovieRateTable WHERE movie_id='{movie_id}'""")
        new_avg = cursor.fetchone()[0]
        
        cursor.execute(
            f"""UPDATE Movie SET average_rate = {new_avg} WHERE id='{movie_id}'"""
        )

        print("your rate added")

        connection.commit()


if __name__ == "__main__":
    mr = MovieRate()
    MovieRate.rate_to_movie("22e0ea34-a5d8-49d6-9e6a-06c1ee927475")
