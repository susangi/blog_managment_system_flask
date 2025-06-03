from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import dbConnection

lesson_admin_bp = Blueprint('lesson_admin', __name__, url_prefix='/admin/lessons')

@lesson_admin_bp.route('/')
def list_lessons():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    
    conn = dbConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lessons ORDER BY id DESC")
    lessons = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('admin/lessons.html', lessons=lessons)

@lesson_admin_bp.route('/create', methods=['POST'])
def create_lesson():
    title = request.form['title']
    description = request.form['description']

    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lessons (title, description) VALUES (%s, %s)", (title, description))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Lesson created successfully.", "success")
    return redirect(url_for('lesson_admin.list_lessons'))

@lesson_admin_bp.route('/delete/<int:id>', methods=['POST'])
def delete_lesson(id):
    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lessons WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Lesson deleted.", "warning")
    return redirect(url_for('lesson_admin.list_lessons'))

@lesson_admin_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_lesson(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    conn = dbConnection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cursor.execute("UPDATE lessons SET title=%s, description=%s WHERE id=%s", (title, description, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Lesson updated successfully.", "info")
        return redirect(url_for('lesson_admin.list_lessons'))

    cursor.execute("SELECT * FROM lessons WHERE id = %s", (id,))
    lesson = cursor.fetchone()
    cursor.close()
    conn.close()

    if not lesson:
        flash("Lesson not found.", "warning")
        return redirect(url_for('lesson_admin.list_lessons'))

    return render_template('admin/edit_lesson.html', lesson=lesson)
