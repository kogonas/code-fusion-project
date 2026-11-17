"""Campus Study Group Finder — Member 1: accounts and profiles."""
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
STYLES = ('Quiet', 'Discussion', 'Problem-solving')
MEETINGS = ('In-person', 'Online', 'Either')
GROUP_SIZES = ('Small', 'Medium', 'Large')
DAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')


def db_connection():
    return mysql.connector.connect(host=os.environ.get('MYSQL_HOST', 'localhost'),
        user=os.environ.get('MYSQL_USER', 'root'), password=os.environ.get('MYSQL_PASSWORD', ''),
        database=os.environ.get('MYSQL_DATABASE', 'campus_study_finder'))


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
            cursor.execute('INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)',
                           (name, email, generate_password_hash(password)))
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


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip().lower()
            if not name or len(name) > 120 or not email or '@' not in email or len(email) > 255:
                flash('Enter a valid name and email.', 'danger')
            else:
                try:
                    cursor.execute('UPDATE users SET name=%s, email=%s WHERE id=%s',
                                   (name, email, session['user_id']))
                    conn.commit()
                    session['name'] = name
                    flash('Profile updated.', 'success')
                except IntegrityError:
                    conn.rollback()
                    flash('That email is already in use.', 'danger')
        cursor.execute('SELECT name, email FROM users WHERE id=%s', (session['user_id'],))
        user = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
    if not user:
        session.clear()
        return redirect(url_for('login'))
    return render_template('profile.html', user=user)


@app.route('/courses', methods=['GET', 'POST'])
@login_required
def courses():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == 'POST':
            code = request.form.get('course_code', '').strip().upper()
            if not code or len(code) > 30:
                flash('Enter a course code (up to 30 characters).', 'danger')
            else:
                try:
                    cursor.execute('INSERT INTO user_courses (user_id, course_code) VALUES (%s, %s)',
                                   (session['user_id'], code))
                    conn.commit()
                    flash('Course added.', 'success')
                except IntegrityError:
                    conn.rollback()
                    flash('You already added this course.', 'warning')
        cursor.execute('SELECT id, course_code FROM user_courses WHERE user_id=%s ORDER BY course_code',
                       (session['user_id'],))
        items = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return render_template('courses.html', courses=items)


@app.route('/courses/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM user_courses WHERE id=%s AND user_id=%s',
                       (course_id, session['user_id']))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    flash('Course removed.', 'success')
    return redirect(url_for('courses'))


@app.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == 'POST':
            style = request.form.get('study_style', '')
            meeting = request.form.get('meeting_type', '')
            size = request.form.get('group_size', '')
            if style not in STYLES or meeting not in MEETINGS or size not in GROUP_SIZES:
                flash('Choose a valid option for each preference.', 'danger')
            else:
                cursor.execute('''INSERT INTO study_preferences (user_id, study_style, meeting_type, group_size)
                    VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE
                    study_style=VALUES(study_style), meeting_type=VALUES(meeting_type),
                    group_size=VALUES(group_size)''', (session['user_id'], style, meeting, size))
                conn.commit()
                flash('Preferences saved.', 'success')
        cursor.execute('SELECT study_style, meeting_type, group_size FROM study_preferences WHERE user_id=%s',
                       (session['user_id'],))
        saved = cursor.fetchone() or {}
    finally:
        cursor.close()
        conn.close()
    return render_template('preferences.html', saved=saved, styles=STYLES, meetings=MEETINGS, sizes=GROUP_SIZES)


@app.route('/availability', methods=['GET', 'POST'])
@login_required
def availability():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == 'POST':
            day = request.form.get('day', '')
            start = request.form.get('start_time', '')
            end = request.form.get('end_time', '')
            # HTML time inputs submit HH:MM; checking the format on the server too.
            import re
            valid_time = lambda t: bool(re.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', t))
            if day not in DAYS or not valid_time(start) or not valid_time(end) or start >= end:
                flash('Choose a day and a valid start/end time.', 'danger')
            else:
                cursor.execute('INSERT INTO user_availability (user_id, day, start_time, end_time) VALUES (%s,%s,%s,%s)',
                               (session['user_id'], day, start, end))
                conn.commit()
                flash('Availability added.', 'success')
        cursor.execute('SELECT id, day, start_time, end_time FROM user_availability WHERE user_id=%s ORDER BY FIELD(day, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"), start_time',
                       (session['user_id'],))
        slots = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return render_template('availability.html', slots=slots, days=DAYS)


@app.route('/availability/<int:slot_id>/delete', methods=['POST'])
@login_required
def delete_availability(slot_id):
    conn = db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM user_availability WHERE id=%s AND user_id=%s',
                       (slot_id, session['user_id']))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    flash('Availability removed.', 'success')
    return redirect(url_for('availability'))


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')
