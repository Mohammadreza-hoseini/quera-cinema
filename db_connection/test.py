from connection import connection


cursor = connection.cursor()
cursor.execute("SELECT * FROM User")
results = cursor.fetchall()
for row in results:
    print(row)
