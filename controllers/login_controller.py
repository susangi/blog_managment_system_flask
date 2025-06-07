from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from db import dbConnection

admin_login_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = dbConnection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
        except Exception as e:
            flash(f"Database error: {e}", "danger")
            return render_template('admin_login.html')
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['admin_logged_in'] = True
            session['username'] = user['username']
            return redirect(url_for('home.dashboard'))  # Ensure correct endpoint here
        else:
            flash('Invalid credentials', 'danger')

    return render_template('admin_login.html')

@admin_login_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('username', None)
    return redirect(url_for('admin.login'))
