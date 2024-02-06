from connection import connection

cursor = connection.cursor()


class Schedule:
    def __init__(self):
        pass

    @classmethod
    def movie_list(cls):
        cursor.execute(
            f'select M.name, M.price, M.age_limit, S.theater_name from Movie M join Schedule S on M.name = S.movie_name')
        movie_list_data = cursor.fetchall()
        for movie_data in movie_list_data:
            print(f'MovieName=>{movie_data[0]}', f'MoviePrice=>{movie_data[1]}', f'MovieAgeLimit=>{movie_data[2]}', f'MovieTheaterName=>{movie_data[3]}', sep='\t')

    @classmethod
    def time_list(cls):

        cursor.execute(
            f'select * from Schedule where on_screen_time >= now() order by on_screen_time desc;')
        time_list_date = cursor.fetchall()

        for i in time_list_date:
            cursor.execute(f'select name from Movie where id = "{i[1]}"')
            movie_name = cursor.fetchone()[0]
            cursor.execute(f'select name from Theater where id = "{i[2]}"')
            theater_name = cursor.fetchone()[0]
            print(i[0], movie_name, theater_name, i[3], sep='|---|')


# Schedule.time_list()
Schedule.movie_list()
