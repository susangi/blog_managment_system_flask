from flask import Blueprint, render_template, request, session, redirect, url_for
from db import dbConnection

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():

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

@home_bp.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    return render_template('admin/dashboard.html')


