from flask import Blueprint, render_template
from db import dbConnection

blog_bp = Blueprint('blog', __name__, url_prefix='/blogs')

@blog_bp.route('/')
def blog_list():
    conn = dbConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, title, caption, updated_at FROM blogs ORDER BY updated_at DESC")
    blogs = cursor.fetchall()

    conn.close()

    return render_template('blog_list.html', blogs=blogs)
