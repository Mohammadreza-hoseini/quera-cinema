from connection import connection

cursor = connection.cursor()


class Sit:
    @staticmethod
    def theater_available_sits(theater_id: str):
        cursor.execute(f"""SELECT id FROM Sit WHERE status='{0}'""")
        data = cursor.fetchall()
        empty_sit_list = []
        for empty_sit_tuple in data:
            empty_sit_list.append(empty_sit_tuple[0])
        return empty_sit_list

    @staticmethod
    def change_status(sit_id: str):
        cursor.execute(f"""SELECT status FROM Sit WHERE id={sit_id.__repr__()}""")
        sit_status = cursor.fetchone()[0]
        if sit_status == "0":
            new_sit_status = "1"
        else:
            new_sit_status = "0"
        cursor.execute(
            f"""UPDATE Sit SET status ={new_sit_status.__repr__()} WHERE id={sit_id.__repr__()}"""
        )

        connection.commit()
        print("Sit status changed")

    def __str__(self):
        pass


if __name__ == "__main__":
    s1 = Sit()
    print(s1.theater_available_sits("970b4d61-b76c-4a57-9ebb-a6967f4fdde5"))
    s1.change_status("f93e4093-c4d3-11ee-874d-0242ac150202")
