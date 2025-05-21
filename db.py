import sqlite3

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect("blog.sqlite")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# SQL query to create the 'posts' table with a created_at timestamp
sql_query = """
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Execute the query
cursor.execute(sql_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Table 'posts' created with automatic timestamp for created_at.")
