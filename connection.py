import mysql.connector
import redis

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

try:
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
except redis.exceptions.ConnectionError as e:
    raise e
