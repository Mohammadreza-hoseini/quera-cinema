from connection import connection

cursor = connection.cursor()
cursor.execute("SELECT * FROM User1")
results = cursor.fetchall()
for row in results:
    print(row)
