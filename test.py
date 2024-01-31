from connection import ConnectionManager

with ConnectionManager() as conn:
    conn.execute("SELECT * FROM User")
    results = conn.fetchall()
    for row in results:
        print(row)
