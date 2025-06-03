from flask import Blueprint, render_template, request
from db import dbConnection

blog_bp = Blueprint('blog', __name__, url_prefix='/blogs')

@blog_bp.route('/')
def blog_list():
    page = int(request.args.get('page', 1))
    per_page = 6  # posts per page
    offset = (page - 1) * per_page

    conn = dbConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM blogs")
    total = cursor.fetchone()['total']
    total_pages = (total + per_page - 1) // per_page

    cursor.execute("""
        SELECT id, title, caption, updated_at 
        FROM blogs 
        ORDER BY updated_at DESC 
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    blogs = cursor.fetchall()

    conn.close()

    return render_template('blog_list.html', blogs=blogs, page=page, total_pages=total_pages)


@blog_bp.route('/<int:blog_id>')
def blog_detail(blog_id):
    conn = dbConnection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, title, content, updated_at FROM blogs WHERE id = %s", (blog_id,))
    blog = cursor.fetchone()

    conn.close()

    if blog:
        return render_template('blog_detail.html', blog=blog)
    else:
        return "Blog not found", 404
