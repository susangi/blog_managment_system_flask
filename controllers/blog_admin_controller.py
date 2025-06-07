from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from db import dbConnection
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename

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
        poster = request.files.get('poster')

        if not poster or poster.filename == '' or not poster.filename.lower().endswith('.png'):
            flash("Poster image is required and must be a .png file.", "danger")
            return redirect(request.url)

        conn = dbConnection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO blogs (title, caption, content, updated_at) VALUES (%s, %s, %s, %s)",
            (title, caption, content, datetime.now())
        )
        conn.commit()
        blog_id = cursor.lastrowid
        cursor.close()
        conn.close()

        # Save poster image as static/img/blogs/{id}/{id}.png
        poster_dir = os.path.join('static', 'img', 'blogs', str(blog_id))
        os.makedirs(poster_dir, exist_ok=True)
        poster_path = os.path.join(poster_dir, f"{blog_id}.png")
        poster.save(poster_path)

        flash("Blog created successfully.", "success")
        return redirect(url_for('blog_admin.list_blogs'))

    return render_template('admin/form_blog.html', blog=None)


@blog_admin_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_blog(id):
    conn = dbConnection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        caption = request.form['caption']
        content = request.form['content']
        poster = request.files.get('poster')

        cursor.execute(
            "UPDATE blogs SET title=%s, caption=%s, content=%s, updated_at=%s WHERE id=%s",
            (title, caption, content, datetime.now(), id)
        )
        conn.commit()

        # Save new poster if uploaded
        if poster and poster.filename.lower().endswith('.png'):
            poster_dir = os.path.join('static', 'img', 'blogs', str(id))
            os.makedirs(poster_dir, exist_ok=True)
            poster_path = os.path.join(poster_dir, f"{id}.png")
            poster.save(poster_path)

        cursor.close()
        conn.close()

        flash("Blog updated successfully.", "info")
        return redirect(url_for('blog_admin.list_blogs'))

    cursor.execute("SELECT * FROM blogs WHERE id = %s", (id,))
    blog = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('admin/form_blog.html', blog=blog)


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

@blog_admin_bp.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    original_filename = secure_filename(image.filename)

    # Get file extension
    ext = os.path.splitext(original_filename)[1]
    # Generate unique filename
    unique_filename = f"{uuid.uuid4().hex}{ext}"

    upload_folder = current_app.config['UPLOAD_FOLDER']
    path = os.path.join(upload_folder, unique_filename)

    # Ensure directory exists
    os.makedirs(upload_folder, exist_ok=True)

    # Save image
    image.save(path)

    # Build public URL
    url = '/' + path.replace('\\', '/')
    return jsonify({'url': url})