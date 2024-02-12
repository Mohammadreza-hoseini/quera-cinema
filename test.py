from connection import connection, redis_client

cursor = connection.cursor()
cursor.execute("SELECT * FROM User")
results = cursor.fetchall()
# print(results)
get_data_from_cache = redis_client.get('schedules')
if get_data_from_cache is None:
    """ request to db for get data """
else:
    """ get data from cache """
    print(get_data_from_cache.decode('utf-8'))
