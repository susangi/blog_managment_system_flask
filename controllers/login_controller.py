from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from db import dbConnection

admin_login_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Dummy credentials
ADMIN_USER = 'admin'
ADMIN_PASS_HASH = 'pbkdf2:sha256:260000$XYZ'  # hashed password

@admin_login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Get user from DB
        conn = dbConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('admin_login.html')

@admin_login_bp.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    return "Welcome to the Admin Dashboard!"

@admin_login_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))
