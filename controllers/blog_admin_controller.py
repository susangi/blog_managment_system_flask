from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import dbConnection
from datetime import datetime

blog_admin_bp = Blueprint('blog_admin', __name__, url_prefix='/admin/blogs')

@blog_admin_bp.route('/')
def list_blogs():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    conn = dbConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM blogs ORDER BY updated_at DESC")
    blogs = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin/blogs.html', blogs=blogs)

@blog_admin_bp.route('/create', methods=['GET', 'POST'])
def create_blog():
    if request.method == 'POST':
        title = request.form['title']
        caption = request.form['caption']
        content = request.form['content']

        conn = dbConnection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO blogs (title, caption, content, updated_at) VALUES (%s, %s, %s, %s)",
            (title, caption, content, datetime.now())
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Blog created successfully.", "success")
        return redirect(url_for('blog_admin.list_blogs'))

    return render_template('admin/create_blog.html')

@blog_admin_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_blog(id):
    conn = dbConnection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        caption = request.form['caption']
        content = request.form['content']
        cursor.execute(
            "UPDATE blogs SET title=%s, caption=%s, content=%s, updated_at=%s WHERE id=%s",
            (title, caption, content, datetime.now(), id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash("Blog updated.", "info")
        return redirect(url_for('blog_admin.list_blogs'))

    cursor.execute("SELECT * FROM blogs WHERE id = %s", (id,))
    blog = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('admin/edit_blog.html', blog=blog)

@blog_admin_bp.route('/delete/<int:id>', methods=['POST'])
def delete_blog(id):
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blogs WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Blog deleted.", "warning")
    return redirect(url_for('blog_admin.list_blogs'))
