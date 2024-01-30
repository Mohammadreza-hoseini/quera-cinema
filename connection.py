import mysql.connector

db_config = {
    "host": "cho-oyu.liara.cloud",
    "port": 32657,
    "user": "root",
    "password": "KILJPqrK7wpJEssWqbO9mv4g",
    "database": "unruffled_lalande",
}


class ConnectionManager:
    def __init__(self, config=db_config):
        self.config = config
        self.db = None

    def __enter__(self):
        try:
            print("db config")

            # Connect to the MySQL database
            self.db = mysql.connector.connect(**(self.config))

            return self.db.cursor()

        except mysql.connector.Error as err:  # connection error
            raise Exception("Connection Error")

    def __exit__(self, type, value, traceback):
        self.db.close()


