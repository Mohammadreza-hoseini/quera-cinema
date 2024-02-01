from connection import connection

cursor = connection.cursor()


class Movie:
    def __init__(self, name, age_limit):
        self.name = name
        self.age_limit = age_limit

    def average_rate(self):
        cursor.execute(f'SELECT AVG(rating) FROM movies WHERE name like "%{self.name}%"')
        return cursor.fetchone()[0]

    def on_screen_count(self):
        cursor.execute(f'SELECT COUNT(*) FROM movies WHERE name like "%{self.name}%"')
        return cursor.fetchone()[0]

    def __str__(self):
        return 'Movie'
