from flask import Blueprint, render_template, session, redirect, url_for

admin_content_bp = Blueprint('admin_content', __name__, url_prefix='/admin')

@admin_content_bp.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    return render_template('admin/dashboard.html')

@admin_content_bp.route('/lessons')
def manage_lessons():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    return render_template('admin/lessons.html')

@admin_content_bp.route('/topics')
def manage_topics():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    return render_template('admin/topics.html')

@admin_content_bp.route('/contents')
def manage_contents():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))

    return render_template('admin/contents.html')
