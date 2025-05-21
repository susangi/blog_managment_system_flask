from flask import Flask, render_template, request, jsonify
import sqlite3

# Create a Flask app instance
app = Flask(__name__)

# In-memory list of blog posts (simulating a database)
posts = [
    {"id": 1, "title": "My First Blog", "author": "Alice", "content": "Welcome to my blog!", "date": "2024-01-01"},
    {"id": 2, "title": "Flask Basics", "author": "Bob", "content": "Let's learn Flask!", "date": "2024-02-15"},
    {"id": 3, "title": "Python Tips", "author": "Charlie", "content": "Useful Python tricks and tips.", "date": "2024-03-20"},
]


# Route to display all blog posts or add a new one
@app.route("/posts", methods=['GET', 'POST'])
def post_list():
   
    if request.method == 'GET':
        
        # Return all posts if available
        if posts is not None:
            return jsonify(posts)
        else:
            return jsonify({"message": "No posts found"}), 404

    if request.method == 'POST':
        # Get new post data from form
        new_title = request.form.get('title')
        new_author = request.form.get('author')
        new_content = request.form.get('content')
        new_date = request.form.get('date')  # Format: YYYY-MM-DD

        # Check for missing fields
        if not all([new_title, new_author, new_content, new_date]):
            return jsonify({"message": "Missing required fields"}), 400

        # Generate a new post ID
        new_id = posts[-1]['id'] + 1 if posts else 1

        # Create new post dictionary
        new_post = {
            "id": new_id,
            "title": new_title,
            "author": new_author,
            "content": new_content,
            "date": new_date
        }

        # Append the new post to the list
        posts.append(new_post)
        return jsonify(new_post), 201

# Route to view, update, or delete a single post by ID
@app.route("/posts/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def single_post(id):
    # Try to find the post by ID
    post = next((p for p in posts if p['id'] == id), None)

    # If post not found, return 404
    if not post:
        return jsonify({"message": "Post not found"}), 404

    if request.method == 'GET':
        # Return the specific post
        return jsonify(post)

    if request.method == 'PUT':
        # Update post details using form data if provided
        post['title'] = request.form.get('title', post['title'])
        post['author'] = request.form.get('author', post['author'])
        post['content'] = request.form.get('content', post['content'])
        post['date'] = request.form.get('date', post['date'])
        return jsonify(post)

    if request.method == 'DELETE':
        # Remove the post from the list
        posts.remove(post)
        return jsonify({"message": f"Post with ID {id} deleted"}), 200

# Route for the home page
@app.route("/")
def home():
    return render_template("index.html")

# Route for blog post management view
@app.route("/post-management")
def post_management():
    return render_template("posts/post_management.html")

# Dynamic route to greet a user by name
@app.route("/<name>")
def greet_user(name):
    return f"Welcome {name}"

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
