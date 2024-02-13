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

    @staticmethod
    def get_all_comments_of_movie():
        movie_name = input('Enter name of movie: ')
        while movie_name == '' or movie_name is None:
            movie_name = input('Enter name of movie: ')
        try:
            cursor.execute(f"SELECT name FROM Movie WHERE name='{movie_name}'")
            result = cursor.fetchone()
            movie_name = result[0]
            print(movie_name)
        except MovieNameDoesNotExist as e:
            print(e)
            return False
        try:
            cursor.execute(f"SELECT id, user_id, created_at, body FROM Comment WHERE movie_name='{movie_name}'")
            results = cursor.fetchall()
            comments_list = []
            for row in results:
                id, user_id, created_at, body = row
                comments_data = {
                    'id': id,
                    'user_id': user_id,
                    'created_at': created_at,
                    'body': body,
                }
                comments_list.append(comments_data)
            print(comments_list)
        except InvalidArguments as e:
            print(e)
            return False

    @staticmethod
    def reply_to_comment(user_id: str, comment_id: str) -> None:
        """ this function for reply to comment """
        ...


comment_manager = Comment()
# comment_manager.get_all_comments_of_movie()
