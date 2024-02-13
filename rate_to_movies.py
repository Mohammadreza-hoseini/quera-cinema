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
        while rate == "" or rate is None:
            rate = input("Enter your rate: ")
        movie_name = input("Enter name of movie: ")
        while movie_name == "" or movie_name is None:
            movie_name = input("Enter name of movie: ")
        try:
            cursor.execute(f"SELECT id FROM Movie WHERE name='{movie_name}'")
            result = cursor.fetchone()
            id = result[0]
        except MovieNameDoesNotExist as e:
            print(e)
            return False
        try:
            cursor.execute(
                f"INSERT INTO MovieRateTable(rate, movie_id, user_id)"
                f"VALUES ('{rate}', '{id}', '{user_id}')"
            )
            connection.commit()
            print("your rate added")
        except InvalidArguments as e:
            print(e)
