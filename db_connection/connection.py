import mysql.connector


try:
    connection = mysql.connector.connect(
        host="cho-oyu.liara.cloud",
        port=32657,
        user="root",
        password="KILJPqrK7wpJEssWqbO9mv4g",
        database="unruffled_lalande",
    )
except mysql.connector.Error as err:
    raise Exception("Connection Error")
# finally:
#     connection.close()
