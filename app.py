from flask import Flask, render_template, request, jsonify
# import sqlite3
from datetime import datetime
import os
import mysql.connector


app = Flask(__name__)

# DB_NAME = 'blog.sqlite'

# Ensure DB and table exist
# def init_db():
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS posts (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             title TEXT NOT NULL,
#             content TEXT NOT NULL,
#             author TEXT NOT NULL,
#             created_at TEXT NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()

# DB Connection helper
def dbConnection():
       return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",           # XAMPP default is empty
        database="blogdb"
    )

# Load posts for rendering HTML
def load_posts(page=1, per_page=4):
    conn = dbConnection()
    cursor = conn.cursor(dictionary=True)

    offset = (page - 1) * per_page

    # Total count
    cursor.execute("SELECT COUNT(*) as total FROM posts")
    total_posts = cursor.fetchone()['total']
    total_pages = (total_posts + per_page - 1) // per_page

    # Fetch paginated posts
    cursor.execute("""
        SELECT * FROM posts
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    posts = cursor.fetchall()
    conn.close()

    return posts, total_pages

# API: GET all posts or POST a new one
@app.route("/api/posts", methods=['GET', 'POST'])
def post_list():
    conn = dbConnection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM posts")
        posts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        if posts:
            return jsonify(posts)
        return jsonify({"message": "No posts found"}), 404

    if request.method == 'POST':
        data = request.get_json()
        new_title = data.get('title')
        new_author = data.get('author')
        new_content = data.get('content')

        if not all([new_title, new_author, new_content]):
            return jsonify({"message": "Missing required fields"}), 400

        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """INSERT INTO posts (title, content, author, created_at) VALUES (?, ?, ?, ?)"""
        cursor.execute(sql, (new_title, new_content, new_author, created_at))
        conn.commit()
        post_id = cursor.lastrowid
        conn.close()
        return jsonify({"message": f"Post with ID {post_id} created successfully"}), 201

# API: GET, PUT, DELETE a single post
@app.route("/api/posts/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def single_post(id):
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id=?", (id,))
    post = cursor.fetchone()

    if not post:
        conn.close()
        return jsonify({"message": "Post not found"}), 404

    if request.method == 'GET':
        result = dict(post)
        conn.close()
        return jsonify(result)

    if request.method == 'PUT':
        data = request.get_json()
        title = data.get('title', post['title'])
        content = data.get('content', post['content'])
        author = data.get('author', post['author'])

        cursor.execute("""
            UPDATE posts SET title=?, content=?, author=? WHERE id=?
        """, (title, content, author, id))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Post with ID {id} updated successfully"}), 200

    if request.method == 'DELETE':
        cursor.execute("DELETE FROM posts WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Post with ID {id} deleted successfully"}), 200

# Web Page: Homepage showing posts
@app.route("/")
def home():
    page = int(request.args.get('page', 1))
    per_page = 4

    posts, total_pages = load_posts(page, per_page)
    return render_template('index.html', posts=posts, page=page, total_pages=total_pages)

# Web Page: Post management
@app.route("/post-management")
def post_management():
    return render_template("posts/post_management.html")

# Initialize and run
if __name__ == '__main__':
    # init_db()
    app.run(debug=True)
