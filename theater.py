from connection import connection

cursor = connection.cursor()


class Theater:

    @staticmethod
    def get_average_rate(theater_name: str) -> float:  # TODO: debug
        """
        Calculates avg_rate for theater_name
        """

        theater_id = Theater.get_theater_id(theater_name)
        cursor.execute(
            f"""SELECT AVG(rate), FROM TheaterRateTable WHERE theater_id={theater_id.__repr__()}"""
        )
        data = cursor.fetchone()
        avg_rate = data[0]
        if avg_rate < 0:
            return "No rate for this theater"
        return avg_rate

    @staticmethod
    def get_theater_id(theater_name: str) -> str:
        """
        returns theater_id from theater_name
        """
        cursor.execute(
            f"""SELECT id FROM Theater WHERE name = {theater_name.__repr__()} """
        )
        return cursor.fetchone()[0]

    @staticmethod
    def update_avg_rate(theater_id: str):
        cursor.execute(
            f"""SELECT AVG(rate) FROM TheaterRateTable WHERE theater_id={theater_id.__repr__()}"""
        )
        new_avg = cursor.fetchone()[0]
        cursor.execute(
            f"""UPDATE Theater SET average_rate={new_avg} WHERE id={theater_id.__repr__()}"""
        )
        connection.commit()

    @staticmethod
    def rate_theater(user_id: str, theater_name: str, rate: int) -> None:
        """
        Add user's rate for theater
        rate can be 1, 2, 3, 4, 5
        """
        theater_id = Theater.get_theater_id(theater_name)

        # Check whether this user rated this theater before
        cursor.execute(
            f"""SELECT 1 FROM TheaterRateTable WHERE theater_id={theater_id.__repr__()} AND user_id={user_id.__repr__()}
                       """
        )

        # rate should be stored as string
        if cursor.fetchone():
            # user's rate should be updated
            cursor.execute(
                f"""UPDATE TheaterRateTable SET rate={str(rate).__repr__()} WHERE theater_id={theater_id.__repr__()} AND user_id={user_id.__repr__()}"""
            )
            print("Your rate is updated")
        else:
            cursor.execute(
                f"""INSERT INTO TheaterRateTable VALUES (%s, %s, {str(rate).__repr__()})""",
                (user_id, theater_id),
            )
            print("Your rate is added")
        connection.commit()
        Theater.update_avg_rate(theater_id)

    @staticmethod
    def theater_name_list():
        cursor.execute("""SELECT name FROM Theater""")
        data = cursor.fetchall()
        theater_name = []
        for name_tuple in data:
            theater_name.append(name_tuple[0])
        print(theater_name)


if __name__ == "__main__":
    t1 = Theater()
    # t1.theater_name_list()
    # t1.rate_theater(
    #     user_id="3075600f-c29c-11ee-9027-0242ac150202", theater_name="valiasr", rate=2
    # )
    # t1.rate_theater(
    #     user_id="99a8fdac-ed21-4d1f-9639-afd6fb68ca7b", theater_name="valiasr", rate=3
    # )
    t1.update_avg_rate(theater_id="41ddc2d2-6613-4a53-96ba-97348496d3b7")
