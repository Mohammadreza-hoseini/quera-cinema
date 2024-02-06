import uuid

from connection import connection

cursor = connection.cursor()


class Movie:
    def __init__(self, name, age_limit):
        self.uuid = uuid.uuid4()
        self.name = name
        self.age_limit = age_limit

    def create_movie(self):
        cursor.execute(f'select name from Movie where name like "%{self.name}%"')
        result = cursor.fetchone()

        if result is not None and self.name in result:
            return "Already exists"
        else:
            print("hi ")
            # return self.on_screen_count()
            cursor.execute(
                f'insert into Movie values (uuid(), "{self.name.__repr__()}",-1 , "{self.on_screen_count()}", "{self.age_limit}")'
            )
            connection.commit()

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
