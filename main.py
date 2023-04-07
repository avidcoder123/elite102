import mysql.connector

connection = mysql.connector.connect(user = "root", database="people", password="thomstarry")


cursor = connection.cursor()

cursor.execute("select * from people;")

for item in cursor:
    print(item)

cursor.close()
connection.close()