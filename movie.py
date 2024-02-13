import uuid

from connection import connection

cursor = connection.cursor()


class Movie:
    def __init__(self, name, age_limit):
        self.uuid = uuid.uuid4()
        self.name = name
        self.age_limit = age_limit

    @staticmethod
    def movie_list():
        cursor.execute(
            f"""SELECT name, average_rate, age_limit, price FROM Movie ORDER BY average_rate DESC"""
        )
        data = cursor.fetchall()

        movie_list = []
        for movie_tuple in data:
            name, average_rate, age_limit, price = movie_tuple
            movie_data = {
                "name": name,
                "average_rate": average_rate,
                "age_limit": age_limit,
                "price": price,
            }
            movie_list.append(movie_data)
        print(movie_list)
        return movie_list

    def average_rate(self) -> str:
        try:
            cursor.execute(
                f'SELECT average_rate FROM Movie WHERE name like "%{self.name}%"'
            )
            return cursor.fetchone()[0]
        except Exception as e:
            return "This movie is not in the database"

    def on_screen_count(self) -> str:
        cursor.execute(f'SELECT COUNT(*) FROM Schedule WHERE movie_id = "%{self.uuid}"')
        return cursor.fetchone()[0]

    def __str__(self):
        return self.name


a = Movie("son of kgod", 18)

a.create_movie()
print(a.average_rate())
