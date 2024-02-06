from connection import connection
from errors import MovieNameDoesNotExist, InvalidArguments

cursor = connection.cursor()


class Comment:
    def __init__(self):
        pass

    @staticmethod
    def add_comment_to_movie(user_id: str) -> str:
        """ this function for add comment to movie """
        body = input('Enter your comment: ')
        while body == '' or body is None:
            body = input('Enter your comment: ')
        movie_name = input('Enter name of movie: ')
        while movie_name == '' or movie_name is None:
            movie_name = input('Enter name of movie: ')
        try:
            cursor.execute(f"SELECT id FROM Movie WHERE name='{movie_name}'")
            result = cursor.fetchone()
            movie_id = result[0]
        except MovieNameDoesNotExist as e:
            print(e)
            return False
        try:
            cursor.execute(f"INSERT INTO Comment(id, user_id, created_at, body, movie_id)"
                           f"VALUES (uuid(), '{user_id}', current_timestamp, '{body}', '{movie_id}')")
            connection.commit()
            print('your comment added')
        except InvalidArguments as e:
            print(e)
