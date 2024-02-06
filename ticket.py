from connection import connection

cursor = connection.cursor()


class Ticket:
    def __init__(self):
        pass

    @classmethod
    def add_ticket(cls, user_id, schedule_id, sit_id):
        # existing user
        cursor.execute(f'select id from User where id = {user_id}')
        user_data = cursor.fetchone()
        if user_data is not None:
            user_date = user_data[0]
        else:
            return "User dose not exists"

        # existing schedule
        cursor.execute(f'select id from Schedule where id = {schedule_id}')
        schedule_data = cursor.fetchone()
        if schedule_data is not None:
            schedule_data = schedule_data[0]
        else:
            return "Schedule dose not exists"

        # existing sit
        cursor.execute(f'select id from sit where id = {sit_id}')
        sit_data = cursor.fetchone()
        if sit_data is not None:
            sit_data = sit_data[0]
        else:
            return "Site dose not exists"


a = Ticket.add_ticket('3075600f-c29c-11ee-9027-0242ac150202'.__repr__(), '1'.__repr__())

print(a)
