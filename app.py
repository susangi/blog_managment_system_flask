from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

# Create Flask app
app = Flask(__name__)

# DB Connection helper
def dbConnection():
    conn = None
    try:
        conn = sqlite3.connect('blog.sqlite')
        conn.row_factory = sqlite3.Row  # For dict-like access
    except sqlite3.error as e:
        print(e)
    return conn

# GET all posts or POST a new post
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
        else:
            return jsonify({"message": "No posts found"}), 404

    if request.method == 'POST':
        new_title = request.form.get('title')
        new_author = request.form.get('author')
        new_content = request.form.get('content')

        if not all([new_title, new_author, new_content]):
            return jsonify({"message": "Missing required fields"}), 400

        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """INSERT INTO posts (title, content, author, created_at) VALUES (?, ?, ?, ?)"""
        cursor.execute(sql, (new_title, new_content, new_author, created_at))
        conn.commit()
        post_id = cursor.lastrowid
        conn.close()

        return jsonify({"message": f"Post with id {post_id} created successfully"}), 201

# GET, PUT, DELETE a single post by ID
@app.route("/api/posts/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def single_post(id):
    conn = dbConnection()
    cursor = conn.cursor()

    # Check if the post exists
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
        title = request.form.get('title', post['title'])
        content = request.form.get('content', post['content'])
        author = request.form.get('author', post['author'])

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

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# Post management page
@app.route("/post-management")
def post_management():
    return render_template("posts/post_management.html")

# Dynamic greeting
@app.route("/<name>")
def greet_user(name):
    return f"Welcome {name}"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
