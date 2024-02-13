from connection import connection

cursor = connection.cursor()


class Movie:

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

    def __str__(self):
        pass


if __name__ == "__main__":
    a = Movie()
    a.movie_list()
