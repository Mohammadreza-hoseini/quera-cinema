from connection import connection

cursor = connection.cursor()


class Theater:

    def __init__(self):
        pass

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
    def rate_theater(user_id: str) -> None:
        """
        Add user's rate for theater
        rate can be 1, 2, 3, 4, 5
        """

        rate = input("Enter your rate: ")
        valid_rates = ["1", "2", "3", "4", "5"]
        while rate not in valid_rates:
            print("Rate should be from 1 to 5")
            rate = input("Enter your rate: ")

        theater_name = input("Enter name of theater: ")
        while theater_name == "" or theater_name is None:
            theater_name = input("Enter name of theater: ")
        cursor.execute(f"SELECT id FROM Theater WHERE name='{theater_name}'")
        result = cursor.fetchone()
        while result is None:
            print("Theater doesn't exist")
            theater_name = input("Enter name of theater: ")
            while theater_name == "" or theater_name is None:
                theater_name = input("Enter name of theater: ")
            cursor.execute(f"SELECT id FROM Theater WHERE name='{theater_name}'")
            result = cursor.fetchone()
        theater_id = result[0]

        # Check whether this user rated this theater before
        cursor.execute(
            f"""SELECT 1 FROM TheaterRateTable WHERE theater_id={theater_id.__repr__()} AND user_id={user_id.__repr__()}
                               """
        )

        # rate should be stored as string
        if cursor.fetchone():
            # user's rate should be updated
            print("You have already rated this theater")
            return

        cursor.execute(
            f"""INSERT INTO TheaterRateTable VALUES (%s, %s, {rate.__repr__()})""",
            (user_id, theater_id),
        )
        print("Your rate is added")

        cursor.execute(
            f"""SELECT AVG(rate) FROM TheaterRateTable WHERE theater_id={theater_id.__repr__()}"""
        )
        new_avg = cursor.fetchone()[0]
        cursor.execute(
            f"""UPDATE Theater SET average_rate={new_avg} WHERE id={theater_id.__repr__()}"""
        )
        connection.commit()

    @staticmethod
    def theater_name_list():
        cursor.execute("""SELECT name FROM Theater""")
        data = cursor.fetchall()
        theater_name = []
        for name_tuple in data:
            theater_name.append(name_tuple[0])
        print(theater_name)


if __name__ == "__main__":
    pass
