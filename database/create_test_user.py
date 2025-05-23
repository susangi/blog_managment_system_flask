from getpass import getpass
from werkzeug.security import generate_password_hash

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db import dbConnection

def create_user():
    username = 'test'
    password_hash = generate_password_hash('test@123')

    conn = dbConnection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        conn.commit()
        print("User created successfully!")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    create_user()
