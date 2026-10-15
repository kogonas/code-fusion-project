"""Sprint 1 starter: registration, login, logout, and protected dashboard."""
import os
from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-me')
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')


def db_connection():
    return mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', 'localhost'),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', ''),
        database=os.environ.get('MYSQL_DATABASE', 'campus_study_finder'),
    )


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


@app.route('/')
def home():
    return redirect(url_for('dashboard' if 'user_id' in session else 'login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if not name or not email or '@' not in email or len(password) < 8:
            flash('Enter a name, valid email, and password of at least 8 characters.', 'danger')
            return render_template('register.html')
        conn = db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)',
                (name, email, generate_password_hash(password)),
            )
            conn.commit()
        except IntegrityError:
            conn.rollback()
            flash('This email is already registered.', 'danger')
            return render_template('register.html')
        finally:
            cursor.close()
            conn.close()
        flash('Account created. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        conn = db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('SELECT id, name, password_hash FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['name'] = user['name']
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=session['name'])


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')
