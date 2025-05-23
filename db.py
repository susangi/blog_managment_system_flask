import mysql.connector

def dbConnection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='blogdb'
    )
    return conn