from connection import connection
from errors import MovieNameDoesNotExist, InvalidArguments

cursor = connection.cursor()


class Comment:
    def __init__(self):
        pass

    @staticmethod
    def add_comment_to_movie(user_id: str) -> str:
        """this function for add comment to movie"""
        body = input("Enter your comment: ")
        while body == "" or body is None:
            body = input("Enter your comment: ")
        movie_name = input("Enter name of movie: ")
        while movie_name == "" or movie_name is None:
            movie_name = input("Enter name of movie: ")
        cursor.execute(f"SELECT name FROM Movie WHERE name='{movie_name}'")
        result = cursor.fetchone()
        while result is None:
            movie_name = input("Enter name of movie: ")
            while movie_name == "" or movie_name is None:
                movie_name = input("Enter name of movie: ")
            cursor.execute(f"SELECT name FROM Movie WHERE name='{movie_name}'")
            result = cursor.fetchone()
        movie_name = result[0]
        cursor.execute(
            f"INSERT INTO Comment(id, user_id, created_at, body, movie_name)"
            f"VALUES (uuid(), '{user_id}', current_timestamp, '{body}', '{movie_name}')"
        )
        connection.commit()
        print("your comment added")

    @staticmethod
    def get_all_comments_of_movie() -> None:
        movie_name = input("Enter name of movie: ")
        while movie_name == "" or movie_name is None:
            movie_name = input("Enter name of movie: ")
        cursor.execute(f"SELECT name FROM Movie WHERE name='{movie_name}'")
        result = cursor.fetchone()
        while result is None:
            print("invalid name of movie")
            movie_name = input("Enter name of movie: ")
            while movie_name == "" or movie_name is None:
                movie_name = input("Enter name of movie: ")
            cursor.execute(f"SELECT name FROM Movie WHERE name='{movie_name}'")
            result = cursor.fetchone()
        movie_name = result[0]
        cursor.execute(
            f"SELECT id, user_id, created_at, body FROM Comment WHERE movie_name='{movie_name}'"
        )
        results = cursor.fetchall()
        if len(result) == 0:
            print("No comment for this movie")
            return
        comments_list = []
        cnt = 0
        print("#### Movie Comments ####")
        print("comment_id, user_id, created_at, body")
        for row in results:
            comment_id, user_id, created_at, body = row
            cnt += 1
            print(f"{cnt}: {comment_id} {user_id} {created_at} {body}")

            comments_data = {
                "id": comment_id,
                "user_id": user_id,
                "created_at": created_at,
                "body": body,
            }
            comments_list.append(comments_data)

    @staticmethod
    def reply_to_comment(user_id: str, comment_id: str) -> None:
        """this function for reply to comment"""
        cursor.execute(
            f"SELECT movie_name FROM Comment WHERE id='{comment_id}' and user_id='{user_id}'"
        )
        result = cursor.fetchone()
        print(result)
        if result is not None:
            body = input("write your reply text: ")
            movie_name = result[0]
            cursor.execute(
                f"INSERT INTO Comment(id, user_id, created_at, body, p_comment_id, movie_name)"
                f"VALUES (uuid(), '{user_id}', current_timestamp, '{body}', '{comment_id}', '{movie_name}')"
            )
            connection.commit()
            print("your comment reply added")
        else:
            print("Invalid arguments")


comment_manager = Comment()
# comment_manager.reply_to_comment('a75d1ce3-78dc-4e60-be8c-5b90c00b09cb', '6ce3f5e7-c4f5-11ee-ad83-0242ac180102')
